

export class UploadQueue {
    constructor(options) {
        // set options
        this.opts = Object.assign(
            {
                dragover: () => {},
                dragleave: () => {},
                announce: (d) => {},
                initialize: (d) => {},
                progress: (d, m) => {},
                success: (d, m) => {},
                warning: (d, m) => {},
                error: (d, m) => {
                    alert(m);
                },
                complete: () => {},
                multiple: true,
            },
            options
        );

        //new implementation

        // file queue
        this.queue = {};

        // queue index/length counter
        this.queue_index = 0;
        this.queue_length = 0;

        // indicates if queue is currently running
        this.queue_running = false;
        this.queue_stop = false;

        // element
        this.uploadinput = options.$uploadBox.uploadinput({
            multiple: this.opts.multiple,
            onchange: (files) => {
                _.each(files, (file) => {
                    file.chunk_mode = true;
                });
                this.add(files);
            },
            ondragover: options.ondragover,
            ondragleave: options.ondragleave,
        });
    }

    // open file browser for selection
    select() {
        this.uploadinput.dialog();
    }

    // remove all entries from queue
    reset() {
        for (const index in this.queue) {
            this.remove(index);
        }
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

    // set options
    configure(options) {
        this.opts = Object.assign(this.opts, options);
        return this.opts;
    }

    // verify browser compatibility
    compatible() {
        return window.File && window.FormData && window.XMLHttpRequest && window.FileList;
    }


    // add new files to upload queue
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

    // remove file from queue
    remove(index) {
        if (this.queue[index]) {
            delete this.queue[index];
            this.queue_length--;
        }
    }

    // process an upload, recursive
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

        const index = this._nextIndex();

        // remove from queue
        this.remove(index);

        // create and submit data
        submitUpload({
            url: this.opts.url,
            data: this.opts.initialize(index),
            success: (message) => {
                this.opts.success(index, message);
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


    _nextIndex() {
        var index = -1;
        for (const key in this.queue) {
            index = key;
            break;
        }
        return index;
    }
}
