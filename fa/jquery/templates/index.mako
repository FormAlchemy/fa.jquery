%if headers:
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>jQuery UI Example Page</title>
    %if mim:
      <link type="text/css" href="/jquery/css/redmond/jquery-ui-1.8.custom.css" rel="stylesheet" />
      <link type="text/css" href="/jquery/fa.jquery.min.css" rel="stylesheet" />	
      <script type="text/javascript" src="/jquery/fa.jquery.min.js"></script>
    %else:
      ${head}
    %endif
	</head>
	<body>
%endif

<style type="text/css">
  form label {font-weight:bold;}
  form .fa_field {margin:1em 0.3em;}
  form {width:50%;}
  .ui-widget {font-size:1em;font-family:'Lucida Grande','Lucida Sans Unicode','Geneva','Verdana',sans-serif;}
</style>
<div>
    <form action="" method="POST">
      <h2>Renderers</h2>
      <p>
      ${fs.render()}
      <div class="ui-widget"><input type="submit" /></div>
      </p>
      <h2>Forms</h2>
      <p>
      <h3>Tabs</h3>
      <div>&nbsp;</div>
      ${tabs.render()}
      </p>
      <p>
      <h3>Accordion</h3>
      <div>&nbsp;</div>
      ${accordion.render()}
      </p>
    </form>
</div>

%if headers:
	</body>
</html>
%endif

