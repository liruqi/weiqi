<script>
    export default {
        methods: {
            form_group_classes(field) {
                return {
                    'has-error': field.dirty && !field.valid,
                    'has-success': field.dirty && field.valid
                }
            }
        }
    }
</script>
