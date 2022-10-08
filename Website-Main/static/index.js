
async function getSP()
{
    let response = await fetch("/safety_programs");
    let result = await response.json();

    return result["Programs"];
}


// Gets text from promise
async function parsePromise(promise)
{
    let value = await promise;

    let program_data = [];
    for(let i = 0; i < value.length; i++)
    {   
        data = [];
        data.push(value[i][0]);
        data.push(value[i][1]);

        program_data.push(data);
    }
    
    return program_data;
}

async function populateUnselected()
{
    let program_data = await parsePromise(getSP());

    unselected_parent = document.getElementById("unselected_parent");

    for(let i = 0; i < program_data.length; i++)
    {   
        //TODO refactor this
        var node = document.createElement("button");
        node.classList.add("program_btn");
        node.classList.add("nonselected_program")

        node.id = "program_" + program_data[i][1];
        node.onclick = moveList;

        var textnode = document.createTextNode(program_data[i][0]);

        node.appendChild(textnode);
        var lineBreak = document.createElement("br");
        lineBreak.id = node.id + "_br";

        unselected_parent.appendChild(node);
        unselected_parent.appendChild(lineBreak);
    }

    var lineBreak = document.createElement("br");
    unselected_parent.prepend(lineBreak);
}

async function moveList()
{   
    old_br = document.getElementById(this.id + "_br");
    old_br.remove();

    parent_id = this.parentNode.id;

    program_btn = document.getElementById(this.id);
    var lineBreak = document.createElement("br");
    lineBreak.id = this.id + "_br";

    if(parent_id == "selected_parent")
    {   
        program_btn.classList.add("nonselected_program");
        program_btn.classList.remove("selected_program");
        parent = document.getElementById("unselected_parent");
    }
    else if(parent_id == "unselected_parent")
    {   
        program_btn.classList.add("selected_program");
        program_btn.classList.remove("nonselected_program");
        parent = document.getElementById("selected_parent");
    }
    
    parent.prepend(program_btn);
    parent.prepend(lineBreak);
}

function searchNonSelected()
{
    let input = document.getElementById('nonselected_query').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('nonselected_program');
      
    for (i = 0; i < x.length; i++) { 
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            console.log(x[i].style.display);
            x[i].style.display="none";

            let br = document.getElementById(x[i].id + "_br");
            br.style.display="none";
        }
        else {
            x[i].style.display="list-item";   
            let br = document.getElementById(x[i].id + "_br");
            br.style.display="list-item";              
        }
    }
}

populateUnselected();
searchNonSelected();
