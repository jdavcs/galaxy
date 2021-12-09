/*
    galaxy upload plugins - requires FormData and XMLHttpRequest
*/

import _ from "underscore";
import jQuery from "jquery";
import { getAppRoot } from "onload/loadConfig";
import * as tus from "tus-js-client";
import axios from "axios";

function submitPayload(payload, cnf) {
    axios
        .post(`${getAppRoot()}api/tools/fetch`, payload)
        .then((response) => {
            cnf.success(response.data);
        })
        .catch((error) => {
            cnf.error(error.response.data.err_msg);
        });
}

/**
 * Posts chunked files to the API.
 */
export function submitUpload(config) {
    // parse options
    var cnf = $.extend(
        {},
        {
            data: {},
            success: () => {},
            error: () => {},
            warning: () => {},
            progress: () => {},
            attempts: 70000,
            timeout: 5000,
            url: null,
            error_file: "File not provided.",
            error_attempt: "Maximum number of attempts reached.",
            error_tool: "Tool submission failed.",
            chunkSize: 10485760,
        },
        config
    );

    // initial validation
    var data = cnf.data;
    if (data.error_message) {
        cnf.error(data.error_message);
        return;
    }
    if (!data.files.length) {
        // No files attached, don't need to use TUS uploader
        return submitPayload(data, cnf);
    }
    const tusEndpoint = `${getAppRoot()}api/upload/resumable_upload/`;
    tusUpload(data, 0, tusEndpoint, cnf);
}

function tusUpload(data, index, tusEndpoint, cnf) {
    const startTime = performance.now();
    const chunkSize = cnf.chunkSize;
    const file = data.files[index];
    if (!file) {
        // We've uploaded all files, delete files from data and submit fetch payload
        delete data["files"];
        return submitPayload(data, cnf);
    }
    console.debug(`Starting chunked upload for ${file.name} [chunkSize=${chunkSize}].`);
    const upload = new tus.Upload(file, {
        endpoint: tusEndpoint,
        chunkSize: chunkSize,
        metadata: data.payload,
        onError: function (error) {
            console.log("Failed because: " + error);
            cnf.error(error);
        },
        onProgress: function (bytesUploaded, bytesTotal) {
            var percentage = ((bytesUploaded / bytesTotal) * 100).toFixed(2);
            console.log(bytesUploaded, bytesTotal, percentage + "%");
            cnf.progress(percentage);
        },
        onSuccess: function () {
            console.log(
                `Upload of ${upload.file.name} to ${upload.url} took ${(performance.now() - startTime) / 1000} seconds`
            );
            data[`files_${index}|file_data`] = {
                session_id: upload.url.split("/").at(-1),
                name: upload.file.name,
            };
            tusUpload(data, index + 1, tusEndpoint, cnf);
        },
    });
    // Check if there are any previous uploads to continue.
    upload.findPreviousUploads().then(function (previousUploads) {
        // Found previous uploads so we select the first one.
        if (previousUploads.length) {
            console.log("previous Upload", previousUploads);
            upload.resumeFromPreviousUpload(previousUploads[0]);
        }

        // Start the upload
        upload.start();
    });
}

(($) => {
    // add event properties
    jQuery.event.props.push("dataTransfer");

    /**
        Handles the upload events drag/drop etc.
    */
    $.fn.uploadinput = function (options) {
        // initialize
        var el = this;
        var opts = $.extend(
            {},
            {
                ondragover: () => {},
                ondragleave: () => {},
                onchange: () => {},
                multiple: false,
            },
            options
        );

        // append hidden upload field
        var $input = $(`<input type="file" style="display: none" ${(opts.multiple && "multiple") || ""}/>`);
        el.append(
            $input.change((e) => {
                opts.onchange(e.target.files);
                e.target.value = null;
            })
        );

        // drag/drop events
        const element = el.get(0);
        element.addEventListener("drop", (e) => {
            opts.ondragleave(e);
            if (e.dataTransfer) {
                opts.onchange(e.dataTransfer.files);
                e.preventDefault();
            }
        });
        element.addEventListener("dragover", (e) => {
            e.preventDefault();
            opts.ondragover(e);
        });
        element.addEventListener("dragleave", (e) => {
            e.stopPropagation();
            opts.ondragleave(e);
        });

        // exports
        return {
            dialog: () => {
                $input.trigger("click");
            },
        };
    };
})(jQuery);

export class UploadQueue {
    constructor(options) {
        // parse options
        this.opts = Object.assign(
            {
                session_id: null,
                dragover: () => {},
                dragleave: () => {},
                announce: () => {},
                initialize: () => {},
                progress: () => {},
                success: () => {},
                warning: () => {},
                error: (d, m) => {
                    alert(m);
                },
                complete: () => {},
                url: null,
            },
            options
        );

        // file queue
        this.queue = {};

        // queue index/length counter
        this.queue_index = 0;
        this.queue_length = 0;

        // indicates if queue is currently running
        this.queue_running = false;
        this.queue_stop = false;

        // element
        this.upload_input = $(options.$uploadBox).uploadinput({
            onchange: (files) => {
                this.add(files);
            },
            ondragover: this.opts.ondragover,
            ondragleave: this.opts.ondragleave,
        });
    }

    // verify browser compatibility
    compatible() {
        return window.File && window.FormData && window.XMLHttpRequest && window.FileList;
    }

    // open file browser for selection
    select() {
        this.upload_input.dialog();
    }

    // initiate upload process
    start() {
        if (!this.queue_running) {
            this.queue_running = true;
            this._process();
        }
    }

    // stop upload process
    stop() {
        this.queue_stop = true;
    }

    // remove file from queue
    remove(index) {
        if (this.queue[index]) {
            delete this.queue[index];
            this.queue_length--;
        }
    }

    // remove all entries from queue
    reset(index) {
        for (index in this.queue) {
            this.remove(index);
        }
    }

    /**
     * Add new files to upload queue
     */
    add(files) {
        if (files && files.length && !this.queue_running) {
            files.forEach((file) => {
                if (_.filter(this.queue, (f) => f.name === file.name && f.size === file.size).length == 0) {
                    const index = String(this.queue_index++);
                    this.queue[index] = file;
                    this.opts.announce(index, this.queue[index]);
                    this.queue_length++;
                }
            });
        }
    }

    /**
     * Process an upload, recursive
     */
    _process() {
        // validate
        if (this.queue_length == 0 || this.queue_stop) {
            this.queue_stop = false;
            this.queue_running = false;
            this.opts.complete();
            return;
        } else {
            this.queue_running = true;
        }

        // get an identifier from the queue
        var index = -1;
        for (const key in this.queue) {
            index = key;
            break;
        }

        // remove from queue
        this.remove(index);

        // create and submit data
        submitUpload({
            url: this.opts.initUrl(index),
            data: this.opts.initialize(index),
            success: (response) => {
                this.opts.success(index, response);
                this._process();
            },
            warning: (message) => {
                this.opts.warning(index, message);
            },
            error: (message) => {
                this.opts.error(index, message);
                this._process();
            },
            progress: (percentage) => {
                this.opts.progress(index, percentage);
            },
        });
    }

    /**
     * xhr request helper
     */
    _upload_request(config) {
        var cnf = Object.assign(
            {
                error_default: "Please make sure the file is available.",
                error_server: "Upload request failed.",
                error_login: "Uploads require you to log in.",
                error_retry: "Waiting for server to resume...",
            },
            config
        );
        console.debug(cnf);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", cnf.url, true);
        xhr.setRequestHeader("Cache-Control", "no-cache");
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhr.setRequestHeader("Accept", "application/json");
        xhr.onreadystatechange = () => {
            if (xhr.readyState == xhr.DONE) {
                if ([502, 0].indexOf(xhr.status) !== -1 && cnf.warning) {
                    cnf.warning(cnf.error_retry);
                } else if (xhr.status < 200 || xhr.status > 299) {
                    var text = xhr.statusText;
                    if (xhr.status == 403) {
                        text = cnf.error_login;
                    } else if (xhr.status == 0) {
                        text = cnf.error_server;
                    } else if (!text) {
                        text = cnf.error_default;
                    }
                    cnf.error(`${text} (${xhr.status})`);
                } else {
                    var response = null;
                    if (xhr.responseText) {
                        response = xhr.responseText;
                    }
                    cnf.success(response);
                }
            }
        };
        xhr.upload.addEventListener("progress", cnf.progress, false);
        xhr.send(cnf.data);
    }
}
