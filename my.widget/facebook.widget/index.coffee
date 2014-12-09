command: "python my.widget/facebook.widget/get-data.py"

# the refresh frequency in milliseconds
refreshFrequency: 1000000

render: -> """
  <h1>Facebook <span class="fb"></span></h1>
"""

update: (output, domEl) ->
  @$domEl = $(domEl)

  #data    = JSON.parse(output)
  data    = output
  @renderFB data

renderFB: (data) ->
  el = @$domEl.find('span.fb')

  id = data?.id

  el.html(data)

style: """
  color: #FFFFFF
  font-family: Helvetica Neue
  left: 12px
  top: 12px

  h1
    font-size: 2em
    font-weight: 100
    margin: 0
    padding: 0
"""
