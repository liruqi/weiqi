<script>
    export default {
        methods: {
            formGroupClasses(field) {
                return {
                    'has-error': field.dirty && !field.valid,
                    'has-success': field.dirty && field.valid
                }
            }
        }
    }
</script>
