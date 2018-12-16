var select = document.getElementsByName('displayData')[0];
select.addEventListener('change',()=>{
    row = task.rows.length;
        if (select.value=="working") {
            for ( var i = 1; i < row; i++ ) {
                if (select.value!=task.rows[i].cells[1].innerText){
                    task.rows[i].style.display = "none";
                } else {
                    task.rows[i].style.display = "";
                }
            }
        } else if (select.value=="finished") {
            for ( var i = 1; i < row; i++ ) {
                if (select.value!=task.rows[i].cells[1].innerText){
                    task.rows[i].style.display = "none";
                } else {
                    task.rows[i].style.display = "";
                }
            }
        } else if (select.value=="notstarted") {
            for ( var i = 1; i < row; i++ ) {
                if(select.value!=task.rows[i].cells[1].innerText){
                    task.rows[i].style.display = "none";
                } else {
                    task.rows[i].style.display = "";
                }
            }
        } else {
            for ( var i = 1; i < row; i++ ) {
                task.rows[i].style.display = "";
            }
        }
})
