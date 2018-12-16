function check() {
    var password = document.regist.password.value;
    var conf = document.regist.confirm.value;
    if ( document.regist.user_name.value == "" ) {
        window.alert('入力データが不足しています');
        return false;
    } else if ( password == "" ) {
        window.alert('入力データが不足しています');
        return false;
    } else if ( conf == "" ) {
        window.alert('入力データが不足しています');
        return false;
    }
    if ( password == conf ) {
        return true;
    } else {
        window.alert('パスワードが一致しません');
        return false;
    }
}
