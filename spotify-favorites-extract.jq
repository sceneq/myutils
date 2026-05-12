.data.me.library.tracks.items[] |
[
  .addedAt.isoString,
  (.track.data.artists.items | map(.profile.name) | join("|")),
  .track.data.name
] | join(",")
