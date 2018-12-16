function check() {
    if(window.confirm("本当に削除していいですか?")) {
        window.alert("削除します");
        return true;
    } else {
        window.alert("キャンセルしました");
        return false;
    }
}
