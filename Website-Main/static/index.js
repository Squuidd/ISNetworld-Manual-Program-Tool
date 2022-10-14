async function getSP() {
    let response = await fetch("/safety_programs");
    let result = await response.json();

    return result["Programs"];
}


// Gets text from promise
async function parsePromise(promise) {
    let value = await promise;

    let program_data = [];
    for (let i = 0; i < value.length; i++) {
        data = [];
        data.push(value[i][0]);
        data.push(value[i][1]);

        program_data.push(data);
    }

    return program_data;
}

async function populateUnselected() {
    let program_data = await parsePromise(getSP());

    unselected_parent = document.getElementById("unselected_parent");

    for (let i = 0; i < program_data.length; i++) {
        //TODO refactor thi

        var btn_node = document.createElement("li");
        btn_node.classList.add("program_btn");
        btn_node.classList.add("nonselected_program")

        btn_node.id = "program_" + program_data[i][1];
        btn_node.onclick = moveList;

        var textnode = document.createTextNode(program_data[i][0]);

        btn_node.appendChild(textnode);

        unselected_parent.appendChild(btn_node);
        btn_node.style.display = "list-item";
    }
}

async function moveList() {
    parent_id = this.parentNode.id;

    program_btn = document.getElementById(this.id);
    if (parent_id == "selected_parent") {
        program_btn.classList.add("nonselected_program");
        program_btn.classList.remove("selected_program");
        parent = document.getElementById("unselected_parent");
    } else if (parent_id == "unselected_parent") {
        program_btn.classList.add("selected_program");
        program_btn.classList.remove("nonselected_program");
        parent = document.getElementById("selected_parent");
    }

    parent.prepend(program_btn);
}

function searchNonSelected() {
    let input = document.getElementById('nonselected_query').value
    input = input.toLowerCase();
    let x = document.getElementsByClassName('nonselected_program');

    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            console.log(x[i].style.display);
            x[i].style.display = "none";
        } else {
            x[i].style.display = "list-item";
        }
    }
}

function searchSelected() {
    let input = document.getElementById('selected_query').value
    input = input.toLowerCase();
    let x = document.getElementsByClassName('selected_program');

    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            console.log(x[i].style.display);
            x[i].style.display = "none";
        } else {
            x[i].style.display = "list-item";
        }
    }
}

function getName() {
    let name = document.getElementById('company_name').value;
    alert(name);
    // check that there is a name
    return name;
}

async function generateDocument(is_manual) {
    let selectedElements = document.getElementsByClassName("selected_program");
    let selectedPrograms = [];

    let company_name = getName();

    for (let i = 0; i < selectedElements.length; i++) {
        selectedPrograms.push(selectedElements[i].innerHTML);
    }

    let data = {
        programs: selectedPrograms,
        manual: is_manual,
        company_name: company_name
    };

    let response = await fetch('/safety_programs',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        }
    )

    // TODO generate names?
    let filename
    if (is_manual) {
        filename = "Manual.docx"
    }
    else {
        filename = "Programs.zip"
    }

    saveBlob(await response.blob(), filename)
}



populateUnselected();

var saveBlob = (function () {
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    return function (blob, fileName) {
        let url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
    };
}());
