command: "python my.widget/gitlab.widget/get-data.py"

# the refresh frequency in milliseconds
refreshFrequency: 1000000

render: -> """
  <h1>GitLab</h1>
  <table class='gl-list'></table>
"""

update: (output, domEl) ->
  @$domEl = $(domEl)
  @renderGL output

renderGL: (data) ->
  el = @$domEl.find('.gl-list')
  el.html('')

  for key, value of JSON.parse data
    @html = @renderRow(key, value)
    if key != 'Error'
      el.append @html
    else
      el.html @html

renderRow: (key, value) ->
  mr_count = if value.requests then value.requests else 0
  mrc_count = if value.comments then value.comments else 0
  mr_has_requests = mr_count > 0
  mrc_has_comments = mrc_count > 0
  return """<tr><td>#{key}</td><td class='gl-mr gl-mr-#{mr_has_requests}'>#{mr_count}</td><td>/</td><td class='gl-mr gl-mr-#{mrc_has_comments}'>#{mrc_count}</td></tr>"""

style: """
  color: #FFFFFF
  font-family: Helvetica Neue
  left: 12px
  top: 56px

  h1
    font-size: 2em
    font-weight: 100
    margin: 0
    padding: 0

  ul
    font-weight: 200
    line-height: 1.4em
    list-style-type: none
    margin: 0
    padding: 0

  .gl-mr
    color: white

  .gl-mr-true
    color: yellow

"""
