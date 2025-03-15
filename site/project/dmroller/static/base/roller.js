

$(document).ready(function() {
    $("#roll_request_form").on("submit", function(event) {
        event.preventDefault(); //prevents page from reloading on form submit
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

    $("#die_roller").on("submit", function(event) {
        event.preventDefault();
        let room_code = $("#room_code").val();
        if (room_code != 'N/A') {
            $("#die_roller_room_code").attr("value", room_code);
        }
        var rollconfig = build_rollconfig();
        if (rollconfig.dice === undefined || rollconfig.dice.length == 0) {
            return;
        } else {
            var die_str = JSON.stringify(rollconfig);
            let submit_roll = $('#die_roller').serializeArray();
            submit_roll.push({name: "roll_config", value: die_str});
            $.post(url_roller, submit_roll, function(roll_result) {
                poll_room();
            });
            resetdie();
        }        
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

function build_rollconfig() {
    let rollconfig = {};
    rollconfig['id'] = '789';
    dieunorderedlist = document.getElementById('die_queue_list');
    dielist = dieunorderedlist.getElementsByTagName('li');
    var _dlist = [];
    for (i=0; i<dielist.length; i++) {
        var count = dielist[i].getAttribute('data-count');
        for (n=0; n<count; n++) {
            die = {};
            die['id'] = dielist[i].getAttribute('id');
            die['faces'] = parseInt(dielist[i].getAttribute('data-faces'));
            die['advantage'] = parseInt(dielist[i].getAttribute('data-advantage'));
            die['reroll_rules'] = [];
            _dlist.push(die);
        }
    }
    rollconfig['dice'] = _dlist;
    modunorderedlist = document.getElementById('modifier_queue_list');
    modlist = modunorderedlist.getElementsByTagName('li');
    var _mlist = [];
    for (i=0; i<modlist.length; i++) {
        modifier = parseInt(modlist[i].getAttribute('data-modifier'));
        _mlist.push(modifier);
    }
    rollconfig['modifiers'] = _mlist;
    return rollconfig;
}

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

var dynamic_count = 1;

function add_removediebutton(id) {
    var _libutton = document.createElement('button');
    _libutton.id = id;
    _libutton.innerHTML = 'Remove';
    _libutton.type = 'button';
    _libutton.setAttribute('onclick', 'removeDie('+id+')');
    _libutton.setAttribute('class', 'listfont');
    return _libutton;
}
function _addDie(faces, advantage, id) {    
    die_queue_list = $("#die_queue_list");       
    if (advantage == -1) {
        _dieadvantage = ' with disadvantage';
    } else if (advantage == 1) {
        _dieadvantage = ' with advantage';
    } else {
        _dieadvantage = '';
    }
    finaladvantage = _dieadvantage
    const dynamic_die_attributes = {
        id: id,
        innerHTML: 'D'+faces+finaladvantage,
    }
    _libutton = add_removediebutton(id);
    var _list = document.getElementById("die_queue_list");
    var _items = _list.getElementsByTagName("li");
    for (i=0; i<_items.length; i++) {
        if ($(_items[i]).attr('data-faces') === faces) {
            if ($(_items[i]).attr('data-advantage') === advantage) {
                var _uniquecount = $(_items[i]).attr('data-count');
                _uniquecount++;
                _items[i].innerHTML = _uniquecount+'D'+faces+finaladvantage;
                _items[i].setAttribute('data-count', _uniquecount);
                _libutton.id = $(_items[i]).attr('id');
                _libutton.setAttribute('onclick', 'removeDie('+_libutton.id+')');
                _items[i].append(_libutton);
                return;
            }
        }        
    }        
    var _li = Object.assign(document.createElement('li'), {...dynamic_die_attributes});
    _li.setAttribute('data-faces', faces);
    _li.setAttribute('data-advantage', advantage);
    _li.setAttribute('data-count', 1);    
    _li.appendChild(_libutton);
    die_queue_list.append(_li);
    dynamic_count++;
}
function removeDie(id) {
    var _die = document.getElementById(id);
    var _uniquecount = _die.getAttribute('data-count');
    var faces = _die.getAttribute('data-faces');
    var advantage = _die.getAttribute('data-advantage');
    if (advantage == -1) {
        _dieadvantage = ' with disadvantage';
    } else if (advantage == 1) {
        _dieadvantage = ' with advantage';
    } else {
        _dieadvantage = '';
    }
    finaladvantage = _dieadvantage
    var _libutton = add_removediebutton(id);
    if (_uniquecount > 2) {
        _uniquecount--;
        _die.innerHTML = _uniquecount+'D'+faces+finaladvantage;
        _die.setAttribute('data-count', _uniquecount);
        _libutton.id = _die.getAttribute('id');
        _libutton.setAttribute('onclick', 'removeDie('+_libutton.id+')');
        _die.append(_libutton);
    } else if (_uniquecount == 2) {
        _uniquecount--;
        _die.innerHTML = 'D'+faces+finaladvantage;
        _die.setAttribute('data-count', _uniquecount);
        _libutton.id = _die.getAttribute('id');
        _libutton.setAttribute('onclick', 'removeDie('+_libutton.id+')');
        _die.append(_libutton);
    } else {
        console.log("Die removed!");
        var _list = document.getElementById("die_queue_list");
        _list.removeChild(_die);
    }
}
function _addModifier(modifier, id) {
    dynamic_count++;
    modifier_queue_list = $("#modifier_queue_list")
    const dynamic_modifier_attributes = {
        id: id,
        innerHTML: modifier,
    }
    var _libutton = add_removediebutton(id);
    _libutton.setAttribute('onclick', 'removeModifier('+id+')');
    var _li = Object.assign(document.createElement('li'), {...dynamic_modifier_attributes});
    _li.setAttribute('data-modifier', modifier);
    _li.appendChild(_libutton);
    modifier_queue_list.append(_li);
}
function removeModifier(id) {
    var _list = document.getElementById("modifier_queue_list");
    var _modifier = document.getElementById(id);
    _list.removeChild(_modifier);
}
function checkoutdie() {    
    let faces = $("#die_faces").val();
    let _radio = document.getElementsByName('die_advantage');
    for (i = 0; i < _radio.length; i++) {
        if (_radio[i].checked) {
            var _advantage =  _radio[i].value; 
        }
    }
    let advantage = _advantage;
    let modifier = $("#modifiers").val();
    if (faces === "" && modifier === "") {
        console.log("Nothing to add to your roll!");
    } else if (modifier === "" && advantage === undefined) {
        console.log("Need to select advantage!")
    } else if (faces === "" && advantage === undefined) {
        _addModifier(modifier, dynamic_count);
        console.log('Modifier added!');
        document.getElementById("die_form").reset();
    } else if (modifier === "") {
        _addDie(faces, advantage, dynamic_count);
        console.log('Die added!');
        document.getElementById("die_form").reset();
    } else {
        _addDie(faces, advantage, dynamic_count);
        _addModifier(modifier, dynamic_count);
        console.log('Die and Modifier added!');
        document.getElementById("die_form").reset();
    }
}
function resetdie() {
    console.log("Die reset!");
    var _dielist = document.getElementById("die_queue_list");
    var _modlist = document.getElementById("modifier_queue_list");
    while(_dielist.firstChild) _dielist.removeChild(_dielist.firstChild);
    while(_modlist.firstChild) _modlist.removeChild(_modlist.firstChild);
}
function savedie() {
    let params = {};
    let roll_config = JSON.stringify(build_rollconfig());
    let roll_name = $('#save_name').val();
    params['roll_config'] = roll_config;
    params['roll_name'] = roll_name;
    $.post(url_save, params, function(result) {
        result = JSON.parse(result);
        if (result['data']) {
            console.log('Save successful!');
            $("#loaded_preset").reload();
        } else {
            console.log('Failed to save');
        }
    })
}
function load_roll_config(roll_config) {
    resetdie();
    roll_config = JSON.parse(roll_config);
    die_list = roll_config["dice"];
    modifier_list = roll_config["modifiers"];
    for (i=0; i<die_list.length; i++) {
        die = die_list[i];
        dynamic_count++;
        let face = die.faces;
        let advantage = die.advantage;
        let id = dynamic_count;
        _addDie(face, advantage, id);
    }    
    for (i=0; i<modifier_list.length; i++) {
        dynamic_count++;
        let modifier = modifier_list[i];
        let id = dynamic_count;
        _addModifier(modifier, id);            
    }    
}