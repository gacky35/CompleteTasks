function check(){
    var flag = 0;
    if ( document.edit.contents.value == "" ) {
        flag = 1;
    } else if ( document.edit.deadline.value == "" ) {
        flag = 1;
    } else if ( document.edit.detail.value == "" ) {
        flag = 1;
    }

    if ( flag ) {
        window.alert('入力データが不足しています');
        return false;
    } else {
        return true;
    }
}
