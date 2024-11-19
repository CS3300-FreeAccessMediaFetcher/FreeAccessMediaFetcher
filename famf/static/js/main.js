const localhost = 'http://localhost:3000/'

function formatLink(link) {

    // link starts with "https://"" 
    if (!link.startsWith("https://")) {
        return "https://" + link;
    }
    return link;
}


// Add  to the table 
function addElementTable(type, name, size, data, checked = true, preview) {

    // Get the table body
    const tableBody = document.querySelector("#output_table tbody");

    // Create a new row
    const newRow = document.createElement("tr");

    // Create cells for Type, Name, Size, Link, Selected, and Preview
    const typeCell = document.createElement("td");
    typeCell.textContent = type;

    // The name of the media
    const nameCell = document.createElement("td");
    nameCell.textContent = name;

    // The size of the media 
    const sizeCell = document.createElement("td");
    sizeCell.textContent = size;

    // Contains the link to the referenced material  
    var formattedLink = formatLink(data)
    const linkCell = document.createElement("td");


    // Create the anchor element for the link
    const anchor = document.createElement("a"); // Make sure `anchor` is declared
    anchor.href = formattedLink; // The source of the content 
    anchor.textContent = "Link"; // Short "link" text to click for the reference of the media.
    anchor.target = "_blank"; // Open in a new tab
    linkCell.appendChild(anchor);


    // Selected cell with a checkbox
    const selectedCell = document.createElement("td");
    const checkbox = document.createElement("input");

    // Create a checkbox of type "checkbox"
    checkbox.type = "checkbox";
    // Make it checked by default
    checkbox.checked = checked;
    // Append checkbox
    selectedCell.appendChild(checkbox);

    // Preview cell
    // Create a cell in the table 
    const previewCell = document.createElement("td");
    // Create the text cell representing the preview

    if (type === "image") {
        //EXAMPLE <img src="img_girl.jpg" alt="Girl in a jacket" width="500" height="600">
        const img = document.createElement("img");

        img.src = formattedLink;
        img.width = 100;
        img.height = 100;
        img.alt = name;

        previewCell.appendChild(img);
    }

    if (type === "text") {
        const p = document.createElement("p");
        p.innerText = data;
        previewCell.appendChild(p)
    }
    
    // Append cells to the new row
    newRow.appendChild(typeCell);
    newRow.appendChild(nameCell);
    newRow.appendChild(sizeCell);
    newRow.appendChild(linkCell);
    newRow.appendChild(selectedCell);
    newRow.appendChild(previewCell);

    // Append the new row to the table body
    tableBody.appendChild(newRow);
    console.log(name + " added to table.");
}


// Remove selected elements from the table
function removeRowFromTable() {
    const tableBody = document.querySelector("#output_table tbody"); // Select the table body by ID
    tableBody.querySelectorAll("tr").forEach(row => { // For each row in the table
        const checkbox = row.querySelector("input[type='checkbox']"); // Selects checkbox in the row
        if (checkbox && checkbox.checked) { // If checkbox is checked
            row.remove(); // Removes the row from the table
        }
    });
}

// removes only checked boxes 
document.getElementById("Remove").addEventListener("click", function (event) {
    // selects the element with .Remove id and adds an on click event to it. for the function :removeRowFromTable()
        event.preventDefault();
        removeRowFromTable();
    });



function returnAllData() {
    const tableBody = document.querySelector("#output_table tbody"); // Select the table body by ID
    var selectedData = []; // array to keet the data.
    var count = 0; // creata a counter for the number of items 
    tableBody.querySelectorAll("tr").forEach(row => { // For each row in the table

        const checkbox = row.querySelector("input[type='checkbox']");
        const rowData = {
            //count = count+1; // iterate the counter.
            // take all atubrutes of the data and place them in to an array 
            type: row.cells[0].innerText,
            name: row.cells[1].innerText,
            size: row.cells[2].innerText,
            link: row.cells[3].innerText
        };
        count = count + 1;
        selectedData.push(rowData);
    });

    if (count == 0) { return null }
    else { return selectedData; }
}

document.getElementById("Download").addEventListener("click", function (event) {
    // selects the element with .Remove id and adds an on click event to it. for the function :removeRowFromTable()
    event.preventDefault(); 
    // download selection by tag "download_raw"/"download_zip"
    const download_raw = document.getElementById("download_raw");
    const download_zip = document.getElementById("download_zip");
    // gather all data
    const selected_data = returnAllData();
    console.log("creating a download request.");
    // if the dataa is not null create a post request :
    if (selected_data != null) {

        if (download_raw.checked) {
            //POST download raw
            console.log("sending post request for download_raw");
            sendDownloadRequestToFlask("download_raw", selected_data);

        } else if (download_zip.checked) {
            //POST download zip
            console.log("sending post request for download_zip");
            sendDownloadRequestToFlask("download_zip", selected_data);
        } else {
            // idf there is no selection in the radio selections for download 
            console.log("unknown error -  radio selection (download zip/raw)")
        }
    } else {
        // if there are no data to push to a post request 
    console.log("no data avaible to post")}
});

function clearTable() {
    // remove all elements from table
    const tableBody = document.querySelector("#output_table tbody");
    tableBody.innerHTML = ""; // Clears all rows in the table
}

// event listener to remove all cells from the table.
document.getElementById("Remove_All").addEventListener("click", function (event) {
    event.preventDefault(); 
    clearTable();
});



const form = document.querySelector("form");
const log = document.querySelector("#log");

form.addEventListener(
    "submit",
    (event) => {
        const data = new FormData(form);
        let output = "";
        for (const entry of data) {
            output = `${output}${entry[0]}=${entry[1]}\r`;
        }
        log.innerText = output;
        event.preventDefault();
    },
    false,
);

function dataTypeSelector() {
    const radios = document.getElementsByClassName('retriever');
    for (let i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            return radios[i].value;
        }
    }
    return null;
}

function getURL() {
    const url = document.getElementById('url_search').value;
    return url;
}



// -------------------- POST
async function sendPostRequestToFlask(url, dataType) {
    const apiEndpoint = localhost;
    const route = 'web-scrape-submission-handler';

    // Create FormData to send to Flask
    const formData = new FormData();
    formData.append("url", url);
    formData.append("data_type", dataType);

    // Send POST request to Flask
    try {
        const response = await fetch(apiEndpoint + route, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            console.error("Server returned error:", response.status);
        }
    } catch (error) {
        console.error("Fetch request failed:", error);
    }
}

async function sendDownloadRequestToFlask(Download_type, data) {
    const apiEndpoint = localhost;
    const zip_route = 'download-manager-zip';
    const raw_route = 'download-manager-raw';
    var route = ""

    //select downloadtype by id corrasoponding to radio button 
    if (Download_type === "download_zip") {
        route = zip_route;

    } else if (Download_type === "download_raw") {
        route = raw_route;
    }

    // Create FormData to send to Flask
    const formData = new FormData();
    formData.append("download_type", Download_type);
    formData.append("data", data);

    try {
        const response = await fetch(apiEndpoint + route, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            console.error("Server returned error:", response.status);
        }
    } catch (error) {
        console.error("Fetch request failed:", error);
    }
}
// -------------------- END POST


document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('search_button');

    searchButton.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent default form submission

        const url = getURL();
        const dataType = dataTypeSelector();

        console.log(`Selected data type: ${dataType}`);
        console.log(`Searching... "${url}"`);

        // Send POST request to Flask
        sendPostRequestToFlask(url, dataType).then(scrapedData => {
            console.log("Scraped data:", scrapedData);

            for (let i = 0; i < scrapedData.length; i++){
                item = scrapedData[i]
                addElementTable(item.dataType,item.dataName, item.dataSize, item.data, true, item.data);
            }
        });
    });
});