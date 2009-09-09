%if headers:
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>jQuery UI Example Page</title>
    ${head}
	</head>
	<body>
%endif

<style type="text/css">
  form label {font-weight:bold;}
  form div {margin:1em;}
  .ui-widget {font-size:1em;font-family:'Lucida Grande','Lucida Sans Unicode','Geneva','Verdana',sans-serif;}
</style>
<div class="ui-widget">
    <form action="" method="POST">
      <h2>Renderers</h2>
      <p>
      ${fs.render()}
      <div><input type="submit" /></div>
      </p>
      <h2>Forms</h2>
      <p>
      <div>&nbsp;</div>
      ${tabs.render()}
      </p>
    </form>
</div>

%if headers:
	</body>
</html>
%endif

