
        $(function () {
            var settings = {
                rows: 5,
                cols: 9,
                rowCssPrefix: 'row-',
                colCssPrefix: 'col-',
                seatWidth: 35,
                seatHeight: 35,
                seatCss: 'seat',
                selectedSeatCss: 'selectedSeat',
				        selectingSeatCss: 'selectingSeat'
            };

            var init = function (reservedSeat) {
                var str = [], seatNo, className;
                for (var i = 0; i < settings.rows; i++) {
                    for (var j = 0; j < settings.cols; j++) {
                        seatNo = (i + j * settings.rows + 1);
                        className = settings.seatCss + ' ' + settings.rowCssPrefix + i.toString() + ' ' + settings.colCssPrefix + j.toString();
                        if ($.isArray(reservedSeat) && $.inArray(seatNo, reservedSeat) != -1) {
                            className += ' ' + settings.selectedSeatCss;
                        }
                        str.push('<li class="' + className + '"' +
                                  'style="top:' + (i * settings.seatHeight).toString() + 'px;left:' + (j * settings.seatWidth).toString() + 'px">' +
                                  '<a title="' + seatNo + '">' + seatNo + '</a>' +
                                  '</li>');
                    }
                }
                $('#place').html(str.join(''));
            };
            var bookedSeats = [5, 10];
            init(bookedSeats);


            // var count = 0;

            $('.' + settings.seatCss).click(function () {
			if ($(this).hasClass(settings.selectedSeatCss)){
				alert('This seat is already reserved');
			}
			else{
			    $(this).toggleClass(settings.selectingSeatCss);
			}
            });

            // $('#btnShow').click(function () {
            //     var str = [];
            //     $.each($('#place li.' + settings.selectedSeatCss + ' a, #place li.'+ settings.selectingSeatCss + ' a'), function (index, value) {
            //         str.push($(this).attr('title'));
            //     });
            //     alert(str.join(','));
            // })

            $('#btnShowNew').click(function () {
                var date = document.getElementById("date-field").value;
                if(date != ""){
                    var str = [], item;
                    var count=0;
                    $.each($('#place li.' + settings.selectingSeatCss + ' a'), function (index, value) {
                        item = $(this).attr('title');
                        str.push(item);
                        count++;
                    });
                    if(count > 1){
                        alert("Please select only one seat")
                    }
                    else if(count === 0){
                        alert("Select a seat")
                    }
                    else {
                        var dropdowntime = document.getElementById("time-field");
                        var dropdowndest = document.getElementById("dest-field");
                        var bustime = dropdowntime.selectedIndex;
                        var destime = dropdowndest.selectedIndex;
                        sendRequest(str[0], date,bustime,destime);
                    }
                }
                else {
                    alert("Please choose a date")
                }

            })
        });

        function sendRequest(seat,date,bustime,dest){
            var csrftoken = getCookie('csrftoken');
            $.ajax({
                type : "POST",
                url : "../registerBus/",
                data : {
                    'csrfmiddlewaretoken': csrftoken,
                    'seat' : seat,
                    'date' : date,
                    'time' : bustime,
                    'dest' : dest
                },
                success : function (data) {
                    alert(data);
                    window.location.reload();
                },
                error : function (e) {
                    alert("Error : " + e.message );
                }
            })
        }

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

