

// Add  to the table 
function addElementTable(type, name, size, link, checked = true, preview) {
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
    const linkCell = document.createElement("td");
   
   
    // Create the anchor element for the link
    const anchor = document.createElement("a"); // Make sure `anchor` is declared
    anchor.href = link; // The source of the content 
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
    previewCell.textContent = preview;
  
    // Append cells to the new row
    newRow.appendChild(typeCell);
    newRow.appendChild(nameCell);
    newRow.appendChild(sizeCell);
    newRow.appendChild(linkCell);
    newRow.appendChild(selectedCell);
    newRow.appendChild(previewCell);
    
    // Append the new row to the table body
    tableBody.appendChild(newRow);
    console.log(name+" added to table.");
  }

  
  //Remove element to the table
  function removeRowFromTable(){
  }

  //remove all elements from table
  function clearTable(){
    const tableBody = document.querySelector("#output_table tbody")
    tableBody.innerHTML ="";
  }

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

async function validateURL(url) {
  try {
    const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
    const response = await fetch(proxyUrl + url, { method: 'GET' });

    if (response.ok) {
      console.log("validate " + url + " = TRUE");
      return true;

    } else {
      console.log("validate " + url + " = FALSE");
      alert("URL invalid");
      return false;
    }

  } catch (error) {
    alert("Request invalid");
    console.log("Error validating URL:", error);
    return false;
  }

}

function dataTypeSelector() {
  const radios = document.getElementsByClassName('retriever');
  for (let i = 0; i < radios.length; i++) {
    if (radios[i].checked) {
      return radios[i].value;
    }
  }
  return null;
}

function getURL(){
  const url = document.getElementById('url_search').value;
  return url;
}

// -------------------- POST
function postToFlask( url, data_type){
  api_endpoint = '/web-scrape-submission-handler';
  user_input = [url, data_type];

  fetch(api_endpoint, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(user_input)
})

}



// Make POST request using fetch
fetch(api_endpoint, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(user_input)
})
.then(response => response.json())  // Parse the JSON from the response
.then(data => {
    console.log('Success:', data);   // Handle the response data
})
.catch((error) => {
    console.error('Error:', error);  // Handle any errors
});

// -------------------- POST

document.addEventListener('DOMContentLoaded', () => { 
  const searchButton = document.getElementById('search_button');
  

  searchButton.addEventListener('click', async (event) => {
    event.preventDefault(); // prevent default form submission
    const url = getURL();
    let data_type = dataTypeSelector();
    console.log("selected dataType value: "+data_type);
    

    
    console.log("searching... \"" + url + "\"");

    if (await validateURL(url)) {
      console.log('URL is valid, proceeding...');
    } else {
      console.error("Invalid URL");
    }

  });
});


  