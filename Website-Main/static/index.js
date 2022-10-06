
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
        var node = document.createElement("button");
        var textnode = document.createTextNode(names[i]);
        node.appendChild(textnode);
        document.getElementById("unselected_parent").appendChild(node);
    }
    //var unselected_html = '<button class="safety_program">test </button>'
}

populateUnselected();
