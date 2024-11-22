const flaskEndpoint = 'http://localhost:3000/'

// UTILITY FUnCTIONS //
function formatLink(link) {

    if (!link.startsWith("https://")) {
        return "https://" + link;
    }
    return link;
}

function getDataType() {
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
// END UTILITY FUNCTIONS //

// BUTTON HANDLERS //
// Select or Deselect all elements in table
function selectAllRows(should_select) {
    const tableBody = document.querySelector("#output_table tbody");
    tableBody.querySelectorAll("tr").forEach(row => { 
        const checkbox = row.querySelector("input[type='checkbox']"); 
        if (checkbox) { 
            checkbox.checked = should_select;
        }
    });
}

document.getElementById("Deselect_All").addEventListener("click", function (event) {
    event.preventDefault();
    selectAllRows(false);
});
document.getElementById("Select_All").addEventListener("click", function (event) {
    event.preventDefault();
    selectAllRows(true);
});

// Remove selected rows 
function removeRowFromTable() {
    const tableBody = document.querySelector("#output_table tbody"); // Select the table body by ID
    tableBody.querySelectorAll("tr").forEach(row => { // For each row in the table
        const checkbox = row.querySelector("input[type='checkbox']"); // Selects checkbox in the row
        if (checkbox && checkbox.checked) { // If checkbox is checked
            row.remove(); // Removes the row from the table
        }
    });
}

// Remove all rows
function removeAllRowsFromTable() {
    // remove all elements from table
    const tableBody = document.querySelector("#output_table tbody");
    tableBody.innerHTML = ""; // Clears all rows in the table
}

document.getElementById("Remove").addEventListener("click", function (event) {
    event.preventDefault();
    removeRowFromTable();
});
document.getElementById("Remove_All").addEventListener("click", function (event) {
    event.preventDefault(); 
    removeAllRowsFromTable();
});

// Download selected data
function returnSelectedData() {
    const tableBody = document.querySelector("#output_table tbody"); // Select the table body by ID
    var selectedData = []; 
    var count = 0;
    tableBody.querySelectorAll("tr").forEach(row => {
        const checkbox = row.querySelector("input[type='checkbox']"); 
        if (checkbox && checkbox.checked) { // Only return checked rows
            const rowType = row.cells[0].innerText
            const rowName = row.cells[1].innerText 
            const rowSize = row.cells[2].innerText
            var rowData = {
                // Take all attributes of the data and place them in to an array 
                type: rowType,
                name: rowName,
                size: rowSize
            };
    
            // For images, add the link to the image. For text, we just need the text itself
            if (rowType == "image") {
                rowData["link"] = row.querySelector("a").getAttribute("href")
            } else if (rowType == "text") {
                rowData["text"] = row.cells[5].innerText
            }
            count = count + 1;
            selectedData.push(rowData);
        }
    });

    if (count == 0) { return null }
    else { return selectedData; }
}

document.getElementById("download_raw").addEventListener("click", function (event) {
    event.preventDefault(); 
    const selected_data = returnSelectedData();
    if (selected_data != null) {
        console.log("sending post request for download_raw");
        sendDownloadRequestToFlask("download_raw", selected_data);
    } else {
        alert("Please select at least one data element to download")
    }
});
document.getElementById("download_zip").addEventListener("click", function (event) {
    event.preventDefault(); 
    const selected_data = returnSelectedData();
    if (selected_data != null) {
        console.log("sending post request for download_raw");
        sendDownloadRequestToFlask("download_zip", selected_data);
    } else {
        alert("Please select at least one data element to download")
    }
});




// -------------------- POST REQUESTS TO FLASK
async function sendPostRequestToFlask(url, dataType) {
    const route = 'web-scrape-submission-handler';

    // Create FormData to send to Flask
    const formData = new FormData();
    formData.append("url", url);
    formData.append("data_type", dataType);

    // Send POST request to Flask
    try {
        const response = await fetch(flaskEndpoint + route, {
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

async function sendDownloadRequestToFlask(download_type, data) {
    const route = 'download-handler';

    // Create FormData to send to Flask
    var postData = {}
    postData["data"] = data
    postData["download_type"] = download_type

    try {
        const response = await fetch(flaskEndpoint + route, {
            method: 'POST',
            body: JSON.stringify(postData),
            headers: { "Content-Type": "application/json" }
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
// -------------------- END POST REQUESTS

// SEARCH HANDLING //
document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('search_button');

    searchButton.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent default form submission

        const url = getURL();
        const dataType = getDataType();

        console.log(`Selected data type: ${dataType}`);
        console.log(`Searching... "${url}"`);

        // Send POST request to Flask
        sendPostRequestToFlask(url, dataType).then(scrapedData => {
            if (typeof(scrapedData) == "object") {
                console.log("Scraped data:", scrapedData);

                for (let i = 0; i < scrapedData.length; i++){
                    item = scrapedData[i]
                    addElementToTable(item.dataType, item.dataName, item.dataSize, item.data, true, item.data);
                }
            }
            else {
                alert("Search failed! Please check URL is valid and try again.")
            }
        });
    });
});

// Add to the table 
function addElementToTable(type, name, size, data, checked = true, preview) {

    const tableBody = document.querySelector("#output_table tbody"); // Get the table body
    const newRow = document.createElement("tr"); // Create a new row

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
    checkbox.type = "checkbox"; // Create a checkbox of type "checkbox"
    checkbox.checked = checked; // Make it checked by default
    selectedCell.appendChild(checkbox); // Append checkbox

    // Create a preview cell in the table 
    const previewCell = document.createElement("td");
    if (type === "image") {
        // EXAMPLE <img src="img_girl.jpg" alt="Girl in a jacket" width="500" height="600">
        const img = document.createElement("img");

        img.src = formattedLink;
        img.width = 100;
        img.height = 100;
        img.alt = name;

        previewCell.appendChild(img);
    }
    else if (type === "text") {
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