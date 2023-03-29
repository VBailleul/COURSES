<head>
    <style>
			table {border: 2px solid black}
			td {border : 2px solid black; text-align:left}
			th {border : 2px solid black}
		</style>
</head>
<body>
    
    <?php
        $pn= ($_GET["pn"]);  //Récupère le prénom
        $n= ($_GET["n"]);       // Récup le nom
        $mel= ($_GET["mel"]); 
        print "<table>
        <tr><td colspan='2'><p>Vous êtes inscrits!</p></td></tr>
        <tr><td><p>Prénom:</p></td><td><p>$pn</p></td></tr>
        <tr><td><p>Nom:</p></td><td><p>$n</p></td></tr>
        <tr><td><p>Mél:</p></td><td><p>$mel</p></td></tr>  
        </table>";
        
        ?>
</body>