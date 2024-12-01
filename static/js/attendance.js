(document).ready(function () {
    const token = localStorage.getItem('access_token');

    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", `Bearer ${token}`);
        }
    });

    const table = $('#attendanceTable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/api/attendances/',
            type: 'GET',
            data: function (d) {
                return {
                    draw: d.draw,
                    start: d.start,
                    length: d.length,
                    search: d.search.value,
                    order: d.order.map(o => ({
                        column: d.columns[o.column].data,
                        dir: o.dir
                    }))
                };
            },
            dataSrc: 'data'
        },
        columns: [
            { data: 'id' },
            { data: 'employee_name' },
            { data: 'date' },
            { data: 'entry_time' },
            { data: 'end_time' },
            { data: 'delayed_time' },
            {
                data: null,
                render: function (data, type, row) {
                    return `
                        <button class="btn btn-sm btn-warning edit-btn" data-id="${row.id}"><i class="fas fa-edit"></i> Edit</button>
                        <button class="btn btn-sm btn-danger delete-btn" data-id="${row.id}"><i class="fas fa-trash"></i> Delete</button>
                    `;
                }
            }
        ],
        language: {
            processing: "Loading...",
            paginate: {
                first: '<<',
                last: '>>',
                next: '>',
                previous: '<'
            }
        },
        pagingType: 'full_numbers'
    });

    $('#addButton').on('click', function () {
        $('#addAttendanceModal').modal('show');
    });

    $('#addAttendanceForm').on('submit', function (e) {
        e.preventDefault();

        const formData = {
            employee: $('#employee').val(),
            date: $('#date').val(),
            entry_time: $('#entry_time').val(),
            end_time: $('#end_time').val(),
            delayed_time: $('#delayed_time').val(),
        };

        $.ajax({
            url: '/api/attendances/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function () {
                $('#addAttendanceModal').modal('hide');
                table.ajax.reload();
                alert('Attendance added successfully!');
            },
            error: function () {
                alert('Failed to add attendance.');
            }
        });
    });
});
