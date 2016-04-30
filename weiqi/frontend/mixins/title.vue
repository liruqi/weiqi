<script>
    export default {
        watch: {
            'windowTitle': function() {
                this.setWindowTitle();
            }
        },

        ready() {
            this.setWindowTitle();
        },

        methods: {
            setWindowTitle() {
                if(!this.windowTitle) {
                    document.title = 'weiqi.gs';
                } else {
                    document.title = this.windowTitle + ' | weiqi.gs';
                }
            }
        }
    }
</script>
