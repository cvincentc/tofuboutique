import $ from 'jquery';

const host = "http://localhost:8000"

const getTags = async (product_token) => {
    var that = this;
    $.ajax({
        url: that.host,
        type: "GET",
        dataType: "json",
        success: (data) => data,
        error: err => err
    });
}