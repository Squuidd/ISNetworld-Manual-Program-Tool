
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
    parent_id = this.parentNode.id;

    program_btn = document.getElementById(this.id);
    var lineBreak = document.createElement("br");

    if(parent_id == "selected_parent")
    {
        parent = document.getElementById("unselected_parent");
    }
    else if(parent_id == "unselected_parent")
    {
        parent = document.getElementById("selected_parent");
    }
    
    parent.prepend(program_btn);
    parent.prepend(lineBreak);

    old_br = document.getElementById(this.id + "_br");
    old_br.remove();
}

populateUnselected();
