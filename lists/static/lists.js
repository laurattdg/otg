(function() {
    function initialize() {
        $('input[name="text"]').on('keypress', function() {
            $('.has-error').hide()
        })
    }
    initialize()
})()