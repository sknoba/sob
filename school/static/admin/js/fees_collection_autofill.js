(function($) {
    $(document).ready(function() {
        $('#id_enrollment').change(function() {
            const enrollmentId = $(this).val();
            const feesStructureField = $('#id_fees_structure');

            if (enrollmentId) {
                $.ajax({
                    url: `/admin/get_fees_structure/`,  // Endpoint to fetch FeesStructure
                    data: { enrollment_id: enrollmentId },
                    success: function(data) {
                        feesStructureField.empty();
                        data.forEach(function(item) {
                            feesStructureField.append(new Option(item.text, item.id));
                        });
                    },
                });
            } else {
                feesStructureField.empty();
            }
        });
    });
})(django.jQuery);
