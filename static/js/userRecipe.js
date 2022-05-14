function bindDeleteBtnClick() {
    $("#delete-btn").on("click", function (event) {
        var $this = $(this);
        console.log("hello,world")
    });
}


// 等网页文档所有元素都加载完成后再执行
$(function () {
    bindDeleteBtnClick();
});