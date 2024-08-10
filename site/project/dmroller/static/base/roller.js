

$(document).ready(function() {
    $("#roll_request_form").on("submit", function(event) {
        event.preventDefault(); //prevents page from reloading on form submit
        var formValues = $(this).serialize();
        //Submits post to 'roll' url with serialized formValues, callback will put results in div with id #result
        $.post(url_roller, formValues, function(roll_result) {
            $("#roll_result").html(roll_result);
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
            }
            else {
                $("#roomcode").text(`Could not join room ${room_code}`);
            }
        })
    })
})

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
