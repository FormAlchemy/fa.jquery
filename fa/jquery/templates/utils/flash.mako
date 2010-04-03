<script language="javascript">
%if onload:
jQuery(document).ready(function () {
%endif
%for message in messages:
jQuery.jGrowl(${message});
%endfor
%if onload:
});
%endif
</script>
