<script>
    export default {
        watch: {
            'window_title': function() {
                this.setWindowTitle();
            }
        },

        ready() {
            this.setWindowTitle();
        },

        methods: {
            setWindowTitle() {
                if(!this.window_title) {
                    document.title = 'weiqi.gs';
                } else {
                    document.title = this.window_title + ' | weiqi.gs';
                }
            }
        }
    }
</script>
