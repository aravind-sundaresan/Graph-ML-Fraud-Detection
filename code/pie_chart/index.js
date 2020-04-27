
var data = {Legitimate: 300, Fradualant: 65};
piechart = new pie_chart(d3.select('.center'), data);

function pie_chart(svg, data){

  this.svg = svg;

	var margin = 40,
	    width = 450,
	    height = 450;
	    pie_width = 300;
	    pie_height = 300;

	var radius = Math.min(pie_width, pie_height) / 2 - margin;	

	var svg = this.svg.append("svg")
	    .attr("width", width )
	    .attr("height", height );
	    

	svg.append("text")
        .text("Distribution of Transactions")
        .attr("x", (width/2))
        .attr("y", 20)        
        .attr("font-family", "sans-serif")
        .attr("font-size", "16px")
        .style("text-anchor", "middle");

	
  var color = d3.scaleOrdinal()
	  .domain(["Legitimate", "Fradualant"])
	  .range(["#008000", "#FF0000"])

	
  this.draw = function(data) {

    piesvg = svg.append("g")
                .attr("transform", "translate(" + pie_width/2 + "," + pie_height/2 + ")");	   

	   var pie = d3.pie();

	   var path = d3.arc()
                     .outerRadius(radius)
                     .innerRadius(0);

     var label = d3.arc()
                      .outerRadius(radius)
                      .innerRadius(radius - 80);


     var arc = piesvg.selectAll(".arc")
                       .data(pie(Object.values(data)))
                       .enter().append("g")
                       .attr("class", "arc");

      arc.append("path")
               .attr("d", path)
               .attr("fill", function(d) { return color(d.index); })
               .attr("stroke", "white")
      			   .style("stroke-width", "2px")
      			   .style("opacity", 1);
        
        
      arc.append("text")
               .attr("transform", function(d) { return "translate(" + label.centroid(d) + ")"; })
               .text(function(d) { t = Object.values(data).reduce(function(a, b){return a + b;}, 0); return Math.round((d.value/t)*100) + '%'; });

               
    	// Add the legend
        svg.selectAll("legend")
            .data(color.domain().slice(0, 2))
            .enter().append("g")
            .append("rect")
            .attr("x", pie_width + 30)
            .attr("y", function(d,n){ return (pie_height/2 + n*25);})
            .attr("width", 15)
            .attr("height", 15)
            .style("fill", function(d) { return color(d);});


        // Add the legend text
        svg.selectAll("legendtext")
            .data(color.domain().slice(0, 2))
            .enter().append("g")
            .append("text")
            .text(function(d){return d;})
            .attr("x", pie_width + 50)
            .attr("y", function(d,n){ return (pie_height/2 + n*25 +11);})
            .attr("font-family", "sans-serif")
            .attr("font-size", "11px");

	}	

	this.draw(data);

}
