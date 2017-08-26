<p> List of Configured Podcasts: </p>
<table border="1">
%for episode_name in episode_list:
    <tr>
        <td><a href="/get_episode/{{ podcast_name }}/{{ episode_name }}">{{ episode_name }}</a></td>
    </tr>
%end
</table>
