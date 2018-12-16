function check(){
    var flag = 0;
    if ( document.add.contents.value == "" ) {
        flag = 1;
    } else if ( document.add.deadline.value == "" ) {
        flag = 1;
    } else if ( document.add.detail.value == "" ) {
        flag = 1;
    }

    if ( flag ) {
        window.alert('入力データが不足しています');
        return false;
    } else {
        return true;
    }
}
