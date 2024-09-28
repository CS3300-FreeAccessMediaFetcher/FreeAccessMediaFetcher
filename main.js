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

  //Remove all elements from table
  function clearTable(){
    const tableBody = document.querySelector("#output_table tbody")
    tableBody.innerHTML ="";
  }
  
  // 
  function addAllToQue(){
    /* 
    when the download box is cheaked:
    add all items to an array 
      */

    // return array 
    }
    const tableBody = document.querySelector("#output_table tbody");
    
   
    function RemoveFromQue(){

    }

    function addAllToQue(){

    }



    function downloadlist (){

        //add all to list : returned array 

        // download each item from array : remove each item from array. 

    }


  