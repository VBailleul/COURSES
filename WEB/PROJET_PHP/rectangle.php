<body>
    <?php
        $l=($_GET["l"]);
        $h=($_GET["h"]);
        $col=($_GET["col"]);
        $couleur=array('bleu'=>'blue', 'vert'=>'green', 'blanc'=>'white');
        $c=$couleur[$col];

        print"
        <svg width='400' height='110'>
            <rect width='$l' height='$h' style='fill:$c;stroke-width:3;stroke:rgb(0,0,0)' />
        </svg>"
    ?>
</body>
