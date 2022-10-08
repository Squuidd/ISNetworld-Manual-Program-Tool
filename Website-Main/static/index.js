
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

    let program_names = [];
    for(let i = 0; i < value.length; i++)
    {
        program_names.push(value[i][0]);
    }
    
    return program_names;
}

async function populateUnselected()
{
    let names = await parsePromise(getSP());

    for(let i = 0; i < names.length; i++)
    {   
        //TODO refactor this
        var node = document.createElement("button");
        node.classList.add("program_btn");
        node.onclick = moveList;

        var textnode = document.createTextNode(names[i]);

        node.appendChild(textnode);
        var lineBreak = document.createElement("br");

        document.getElementById("unselected_parent").appendChild(node);
        document.getElementById("unselected_parent").appendChild(lineBreak);
    }
}

async function moveList()
{
    alert(this);

}

populateUnselected();
