/** initialize the table for whole-cycle counts 
 * @param {string} detector Li6|He3|He3Det2 
*/
async function init_count_table(detector){

    // get the table
    let table = document.getElementById(`${detector}_table`);

    // header row
    let row = table.insertRow();
    let cell = row.insertCell();
    cell.className = 'mtableheader';
    cell.innerText = 'Cycle Start Time';
    cell.style.width = '250px';
    
    cell = row.insertCell();
    cell.className = 'mtableheader';
    cell.innerText = 'UCN Counts';
    cell.style.width = '250px';

    // body 
    for(let i=0; i<10; i++){
    row = table.insertRow();

    // cycle start times
    cell = row.insertCell();
    let div = document.createElement('div');
    div.className = 'modbvalue';
    div.style.textAlign = 'center';
    div.setAttribute('data-odb-path', `/Analyzer/${detector}/CycleStartTimes[${9-i}]`)
    cell.appendChild(div);

    // counts
    cell = row.insertCell();
    div = document.createElement('div');
    div.className = 'modbvalue';
    div.style.textAlign = 'right';
    div.setAttribute('data-odb-path', `/Analyzer/${detector}/UCNHitsPerCycle[${9-i}]`)
    cell.appendChild(div);
    }
}

/** initialize the table for period and cycle counts 
 * @param {string} detector Li6|He3|He3Det2 
*/
async function init_period_table(detector){

    // get table
    let table = document.getElementById(`${detector}_period_table`);

    // header row
    let row = table.insertRow();

    let cell = row.insertCell();
    cell.className = "mtableheader";
    cell.innerText = 'Cycle Start Time';

    cell = row.insertCell();
    cell.className = "mtableheader";
    cell.innerText = 'Cycle Number';

    cell = row.insertCell();
    cell.className = "mtableheader";
    cell.innerText = 'UCN Counts Per Period';
    cell.colSpan = '10';
    
    // title row
    row = table.insertRow();
    
    cell = row.insertCell();
    cell.style.width = '200px'; 
    
    cell = row.insertCell();
    cell.style.width = '150px'; 

    for(let i=0; i<10; i++){
    cell = row.insertCell();
    cell.innerText = i;
    cell.style.width ='60px';
    cell.style.textAlign ='center';
    cell.style.fontWeight = 'bold';
    }

    // data rows
    for(let i=0; i<10; i++){
    row = table.insertRow();

    // start time
    cell = row.insertCell();
    let div = document.createElement('div');
    div.className = "modbvalue";
    div.style.textAlign = 'center';
    div.setAttribute('data-odb-path', `/Analyzer/${detector}/CycleStartTimes[${9-i}]`);
    cell.appendChild(div);

    // id
    cell = row.insertCell();
    cell.id = `cycle_id_${detector}_row${i}`;
    cell.style.textAlign = 'center';

    // counts
    for(let j=0; j<10; j++){
        cell = row.insertCell();
        let div = document.createElement('div');
        div.className = "modbvalue";
        div.style.textAlign = 'right';
        div.setAttribute('data-odb-path', `/Analyzer/${detector}/UCNHitsPerCyclePeriod${j}[${9-i}]`);
        cell.appendChild(div);
    }
    }
}
