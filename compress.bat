@echo off
setlocal
cd fa/jquery/jquery-ui-1.8rc1.custom
type css\*.css >fa.jquery.min.css
type js\jquery-*.js js\jquery.*.js colorpicker\*.js markitup\*.js >fa.jquery.min.js
endlocal
