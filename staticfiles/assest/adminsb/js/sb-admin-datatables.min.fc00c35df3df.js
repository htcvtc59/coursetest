$(document).ready(function () {
    $("#dataTableLoadData").DataTable({
        "language": {
            "decimal": "",
            "emptyTable": "Không có dữ liệu trong bảng !",
            "info": "Showing _START_ to _END_ of _TOTAL_ entries",
            "infoEmpty": "Showing 0 to 0 of 0 entries",
            "infoFiltered": "(tìm thấy từ _MAX_ số bản ghi)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Show _MENU_ entries",
            "loadingRecords": "Loading...",
            "processing": "Processing...",
            "search": "Tìm kiếm:",
            "zeroRecords": "Không có bản ghi nào !",
            "paginate": {
                "first": "Đầu tiên",
                "last": "Cuối cùng",
                "next": "Tiếp theo",
                "previous": "Trở lại"
            },
            "aria": {
                "sortAscending": ": activate to sort column ascending",
                "sortDescending": ": activate to sort column descending"
            }

        }
    });
});
