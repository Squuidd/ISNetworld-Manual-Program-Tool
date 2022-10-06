
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
        var unselected_html = '<button></button>'
    }

    document.getElementById("unselected_programs").innerHTML = val[0];
}

populateUnselected();
