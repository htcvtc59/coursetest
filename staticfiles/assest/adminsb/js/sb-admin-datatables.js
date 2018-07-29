// Call the dataTables jQuery plugin
$(document).ready(function () {
    $(".dataTableLoadData").DataTable({
        "pagingType": "full_numbers",
        "language": {
            "decimal": "",
            "emptyTable": "Không có dữ liệu trong bảng !",
            "info": "Bản ghi từ _START_ đến _END_ của _TOTAL_ số bản ghi",
            "infoEmpty": "Showing 0 to 0 of 0 entries",
            "infoFiltered": "(tìm thấy từ _MAX_ số bản ghi)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Hiển thị _MENU_ bản ghi",
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
