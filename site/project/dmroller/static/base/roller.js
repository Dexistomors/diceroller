

$(document).ready(function() {
    $("#roll_request_form").on("submit", function(event) {
        event.preventDefault(); //prevents page from reloading on form submit
        console.log('1');
        //console.log(formValues);
        let room_code = $("#room_code").val();
        if (room_code != 'N/A') {
            $("#roll_request_room_code").attr("value", room_code);
        }
        let formValues = $(this).serialize();
        //Submits post to 'roll' url with serialized formValues, callback will put results in div with id #result
        $.post(url_roller, formValues, function(roll_result) {
            //$("#roll_result").html(roll_result);
            poll_room();
        })
    })

    $("#room_request_form").on("submit", function(event) {
        event.preventDefault();
        let formValues = $(this).serialize();
        $.post(url_room, formValues, function(result) {
            result = JSON.parse(result);
            let room_code = $("#room_code").val();
            if (result['data'] == 'success') {
                $("#roomcode").text(room_code);
                update_room_users();
            }
            else {
                $("#roomcode").text(`Could not join room ${room_code}`);
            }
        })
    })

    setInterval(poll_room, 5000);

})

function poll_room() {
    let room_code = $("#room_code").val();
    if (room_code != 'N/A') {
        let params = {};
        params['room_code'] = room_code;
        if ($('#roll_result').attr('data-last-timestamp')) {
            params['date'] = $('#roll_result').attr('data-last-timestamp');
        }
        $.get(url_room, params, function(result) {
            result = JSON.parse(result);
            if ('data' in result) {
                let roll_results = result['data']['roll_results'];
                roll_results.forEach(function(r) {
                    let tmp = `${r['date']}: ${r['user']}: ${r['prettify']}`;
                    $('<div/>',{
                        'text': tmp,
                        'class': 'rollresponse',
                        'data-timestamp': r['date']
                    }).appendTo('#roll_result')
                });
                if (roll_results.length) {
                    let most_recent_date = roll_results[roll_results.length - 1]['date'];
                    $('#roll_result').attr('data-last-timestamp', most_recent_date);
                }                
            } else {
                console.log('Failed to fetch roll_results from room');
            }
        });
    }
}

function update_room_users() {
    let params = {};
    let room_code = $("#room_code").val();
    params['room_code'] = room_code;
    params['users'] = 'yes';
    $.get(url_room, params, function(result) {
        result = JSON.parse(result);
        if ('data' in result) {
            let usernames = result['data'].sort().join(',');
            $('#roompop').text(usernames);
        } else {
            console.log('Failed to fetch users from room');
        }
    })
}

var dynamic_input_count = 1;
function adddie() {
    dynamic_input_count++;

    var input_div = $("#die_list");
    var new_input_id = "die_" + dynamic_input_count;
    var new_p = document.createElement("p");
    
    new_p.textContent = "Faces: ";

    var new_input = document.createElement("input");
    new_input.setAttribute("id", new_input_id);
    new_input.setAttribute("type", "number");
    new_input.setAttribute("class", "intinput");
    new_input.setAttribute("min", "2");

    new_p.append(new_input);
    input_div.append(new_p);

    var new_p2 = document.createElement("p");
    new_p2.innerHTML = "Advantage:<br>";
    const advantage = {
        "Disadvantage": false,
        "No Advantage": false,
        "Advantage": false,
    }
    for (let key in advantage) {
        let label = document.createElement("label");
        label.innerText = key;
        label.setAttribute("class", "listfont");
        label.setAttribute("for", "advantage");

        let input = document.createElement("input");
        input.setAttribute("id", new_input_id);
        input.setAttribute("class", "radio");
        input.setAttribute("name", "advantage");
        input.type = "radio";
        input.name = new_input_id;

        input.addEventListener('change', () => {
            Object.keys(data).forEach(key => {
                data[key] = false;
            })
            data[key] = true;
        });

        new_p2.appendChild(input);
        new_p2.appendChild(label);
    }
    input_div.append(new_p2);
}
function addmodifier() {
    var input_div = $("#modifier_list");
    var new_p = document.createElement("p");
    
    new_p.textContent = "Modifier: ";

    var new_input = document.createElement("input");
    new_input.setAttribute("type", "number");
    new_input.setAttribute("class", "intinput");

    new_p.append(new_input);
    input_div.append(new_p);
}
function jsDie(faces, advantage, id) {
    this.faces = faces;
    this.advantage = advantage;
    this.id = id
}
function jsModifier(modifier, id){
    this.modifier = modifier;
    this.id = id
}
var dynamic_modifier_count = 1;
var dynamic_die_count = 1;
var dynamic_die_list = [];
var dynamic_modifier_list = [];

function _addDie(faces, advantage, dynamic_die_count) {
    die_queue_list = $("#die_queue_list")
    dynamic_die_list.push(jsDie(faces, advantage, dynamic_die_count));
    for (i=0; i < dynamic_die_list.length; i++) {
        for (faces in dynamic_die_list[i]);
            _dieFace = faces;
        if (dynamic_die_count > i) {      
            var newDiv = document.createElement("p");
            newDiv.innerHTML = ('<li> D'+_dieFace+'</li>');
        }
    }
    die_queue_list.append(newDiv);
    dynamic_die_count++;
}
function _addModifier(modifier, dynamic_modifier_count) {
    modifier_queue_list = $("#modifier_queue_list")
    dynamic_modifier_list.push(jsModifier(modifier, dynamic_modifier_count));
    for (i=0; i < dynamic_modifier_list.length; i++) {
        for (modifier in dynamic_modifier_list[i]);
            _dieModifier = modifier;
        if (dynamic_modifier_count > i) {
            var newDiv2 = document.createElement("p");
            newDiv2.innerHTML = ('<li>'+_dieModifier+'</li>');
        }
    }
    modifier_queue_list.append(newDiv2);
    dynamic_modifier_count++;
}
function checkoutdie() {
    let faces = $("#die_faces").val();
    let _radio = document.getElementsByName('die_advantage');
    for (i = 0; i < _radio.length; i++) {
        if (_radio[i].checked)
            var _advantage =  _radio[i].value;
    }
    let advantage = _advantage
    let modifier = $("#modifiers").val();
    console.log(modifier);
    if (faces === "" && advantage === undefined && modifier === "") {
        console.log("Nothing to add to your roll!");
    } else if (faces === "" && advantage == undefined) {
        _addModifier(modifier, dynamic_modifier_count);
        console.log('Modifier added!');
        document.getElementById("die_form").reset();
    } else if (modifier === "" ) {
        _addDie(faces, advantage, dynamic_die_count);
        console.log('Die added!');
        document.getElementById("die_form").reset();
    } else {
        _addDie(faces, advantage, dynamic_die_count);
        _addModifier(modifier, dynamic_modifier_count);
        console.log('Die and Modifier added!');
        document.getElementById("die_form").reset();
    }
}      


