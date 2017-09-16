<p> List of Configured Podcasts: </p>
<table border="1">
%for name,url in rows:
    <tr>
        <td><a href="/get_podcast/{{ name }}">{{ name }}</a></td>
        <td>{{ url }}</td>
    </tr>
%end
</table>
