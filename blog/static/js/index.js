var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        is_login:true,
        username:''
    },
    mounted(){
        //获取用户名信息
        this.username=getCookie('username');
        //获取是否登录信息
        this.is_login=getCookie('is_login');
    },
    methods: {
        //显示下拉菜单
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        },
    }
});
