function snake_eat() {

    var sn = [42, 41], dz = 43, fx = 1, n, ctx = document.getElementById("snakeat_can").getContext("2d");

    function gameover() {
        ctx.fillStyle = "Black";
        ctx.fillRect(0,0,400,400);

    }
    function draw(t, c) {
        ctx.fillStyle = c;//填充颜色样式
        ctx.fillRect(t % 20 * 20 + 1, ~~(t / 20) * 20 + 1, 20, 20);//图像生成位置  小于20px可以显示格子蛇
    }

    document.onkeydown = function (e) {
        fx = sn[1] - sn[0] == (n = [-1, -20, 1, 20][(e || event).keyCode - 37] || fx) ? fx : n
    };
    !function () {
        sn.unshift(n = sn[0] + fx);//
        if (sn.indexOf(n, 1) > 0 || n < 0 || n > 399 || fx == 1 && n % 20 == 0 || fx == -1 && n % 20 == 19)
            return gameover();
        draw(n, "Lime");
        if (n == dz) {
            while (sn.indexOf(dz = ~~(Math.random() * 400)) >= 0) ;
            draw(dz, "Yellow");
        } else
            draw(sn.pop(), "Black");
        setTimeout(arguments.callee, 130);//蛇运动速度
    }();
}