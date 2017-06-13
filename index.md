## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/delgadom/playground/edit/master/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

<html>

<head>
  <title>Map Gen</title>

  <!-- online mode -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.9.1/d3.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.0/topojson.min.js"></script>
  <script
  src="https://code.jquery.com/jquery-3.2.1.min.js"
  integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4="
  crossorigin="anonymous"></script>

  <!-- offline mode -->
  <!-- to prepare, run:

      mkdir lib
      curl https://cdnjs.cloudflare.com/ajax/libs/d3/4.9.1/d3.min.js > lib/d3.min.js
      curl https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.0/topojson.min.js > lib/topojson.min.js
      curl https://code.jquery.com/jquery-3.2.1.min.js > lib/jquery-3.2.1.min.js

   -->
  <!-- <script src="lib/d3.min.js"></script>
  <script src="lib/topojson.min.js"></script>
  <script src="lib/jquery-3.2.1.min.js"></script> -->


  <link href="./style.css" media="all" rel="stylesheet" />
</head>

<body>

  <div class="acf-map-generator__controls">
    <h5>Controls</h5>
    Show 

    <select id="combobox-variable">
      <option value="tas_DJF">Dec-Jan-Feb avg temp</option>
      <option value="tas_MAM">Mar-Apr-May avg temp</option>
      <option value="tas_JJA" selected>Jun-Jul-Aug avg temp</option>
      <option value="tas_SON">Sep-Oct-Nov avg temp</option>
      <option value="tasmax">days with max temp over 95F</option>
      <option value="tasmin">days with min temp under 32F</option>
    </select>
    
     as 
    <select id="combobox-relative">
      <option value="absolute">absolute values</option>
      <option value="change-from-hist">change from historical</option>
    </select>
     at 
    <select class="global-dataset-percentile-list" id="global-dataset-percentile-list">
			<option value="0.05">1-in-20 low</option>
			<option value="0.5" selected>median</option>
			<option value="0.95">1-in-20 high</option>
		</select>

    probability

    <br />
    <input type="range" id="period-slider" value="3" step="1" min="0" max="3" data-show-value="true">
    <div><span class="period">Period: </span><span class="period" id="period-value">2080 to 2099</span></div>
    <br />

    <button class="button generate-map" id="generate-map">Re-generate Map</button>

  </div>
  <div class="acf-map-generator__map-preview">
    <h5>Map Preview</h5>
  </div>

</body>

<script src="d3-map.js"></script>



For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/delgadom/playground/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
