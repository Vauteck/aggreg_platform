<html lang="en">
<head>
<style type="text/css">
#entete, #menu, #itf-text-area-div, #itf-save-load-div, #footer {
	margin:10px 10px 10px 10px;
}
#page_title {
	text-align:center;
}
#main {
}
#itf-text-area-div  {
	display: inline-block;
	float: left;
}
#itf-save-load-div {
	display: inline-block;
	float: left;
}
#scenario-menu-div {
	margin-left: 20px;
	display: inline-block;
	float: left;
}
#general-scenario-resume {
	margin-left: 20px;
	float: left;
}
#execute-shell-command {
	margin-left: 20px;
	display: block;
	float: left;
}
#footer {
	text-align:center;
	clear:both;
}
#scenario-config {
	display: none;
}
#scenario-editor {
	display: none;
}

</style>
<?php
	session_start();
	// init itf list
	$itf_list = array();
	$cmd = "/sbin/ifconfig | /bin/grep eth | awk '{print $1;}'";
	exec($cmd, $itf_list);

	// are there scenario scripts already running ? (enable/disable stop button)
	$cmd = "ps -e | /bin/grep php";
	exec($cmd, $script_process_list);
?>
<script type="text/javascript" src="scripts/jquery-1.8.3.min.js"></script>
<script type="text/javascript">
	scenario_list = '';
	generic_scenario_list = '';
	general_scenario_pid_list = new Array();

	function change_menu(val) 
	{
		//alert(val);
		$("#static-conf").hide();
		$("#scenario-config").hide();
		$("#scenario-editor").hide();

		var select = document.getElementById("load_rules_file_select");
		select.options.length = 0;
		for(var i = 0; i < scenario_list.length; i++)
    		select.options[select.options.length] = new Option(scenario_list[i], scenario_list[i]);
		
		var select = document.getElementById("load_general_scenario_select");
		select.options.length = 0;
		for(var i = 0; i < generic_scenario_list.length; i++)
    		select.options[select.options.length] = new Option(generic_scenario_list[i], generic_scenario_list[i]);

		if(val == 'config')
		{
			$("#scenario-config").show();
			return;
		}
		if(val == 'editor')
		{
			$("#scenario-editor").show();
			return;
		}
		$("#static-conf").show();
	}

	function isNumberKey(evt)
    {
    	var charCode = (evt.which) ? evt.which : event.keyCode
    	if (charCode > 31 && (charCode < 48 || charCode > 57))
        	return false;
 
         return true;
    }

	function addTextLine(data, el) {
		if (el.value != '')
			el.value += '\n';
		el.value += data;
	}

	function select1_change(val) {
		list_itf_scenario(val);
	}

    $(function()
    {
      	$('#add_text_line').click(function()
      	{
			var data_line = time_form.value+', '+bandwidth_form.value+', '+latency_form.value+', '+jitter_form.value+', 1000, '+loss_form.value;
        	addTextLine(data_line, rules_file_content);
      	});
    });

    function download_to_textbox(url, el)
    {
		el.value = '';
		$.ajax({ 
    		url: url, 
    		dataType: "text",
			cache: false,
    		success: function(data) {
      			el.value = data;
			}
		});
    }

    $(function()
    {
      	$('#load_rules_file_button').click(function()
      	{
        	download_to_textbox('scenarios//'+load_rules_file_select.value, rules_file_content);
			if(save_rules_file_namebox.value == '')
				save_rules_file_namebox.value = load_rules_file_select.value;
		});
    });

	$(function()
	{
		$('#add_script_scenario').click(function()
      	{
			var datarow = generaterow($("#config_select_interface").val(), $("#select_scenario_list").val());
			var rows = $('#jqxgrid').jqxGrid('getrows');
			var position = rows.length;
			for(var i=0, l=rows.length; i<l; i++)
			{
				if(rows[i]['interface'] == $("#config_select_interface").val())
				{
					$("#jqxgrid").jqxGrid('deleterow', i);
					position = i;
					break;
				}
			}
			var commit = $("#jqxgrid").jqxGrid('addrow', null, datarow, position);
		});
	});
	
	$(function()
	{
		$('#launch_general_scenario_config').click(function()
		{
			$('#stop_general_scenario_config').attr("disabled", false);
			$('#launch_general_scenario_config').attr("disabled", true);
			var itfScenarioArray = JSON.stringify(getGeneralConfigValue());
			$.ajax({
				type: "POST",
				url: "run_general_scenario.php",
				dataType: "json",
				data: { "itf" : itfScenarioArray, "loop" : $('#loop_general_scenario_checkbox').is(":checked") },
				success: function(data)
				{
				}
			});
		});
	});

	$(function()
	{
		$('#stop_general_scenario_config').click(function()
		{
			$('#stop_general_scenario_config').attr("disabled", true);
			$('#launch_general_scenario_config').attr("disabled", false);
			$.ajax({
				type: "POST",
				url: "kill_general_scenario.php",
				success: function(data) 
				{
				}
			});
		});
	});

	function reset_interface(itf)
    {
        $.ajax({
			type: "POST",
    		url: "reset_interface.php",
			data: {"itf":itf}
		});
   	}

	function apply_static_conf(bandwidth, latency, jitter, loss, itf)
	{
       	$.ajax({
			type: "POST",
   			url: "apply_conf.php",
   			data: {"bandwidth":bandwidth,"delay":latency,"jitter":jitter,"loss":loss,"itf":itf}//,
		});
	}

	function update_scenario_list()
	{
		var dir = 'scenarios';
		$.ajax({
			type: "POST",
   			url: "list_dir_files.php",
   			data: {"dir":dir},
			success: function(data) {
				if(data.length != 0)
					scenario_list = data.match(/[^\r\n]+/g);
			}
		});
	}

	function update_generic_scenario_list()
	{
		var dir = 'general_scenarios';
		$.ajax({
			type: "POST",
   			url: "list_dir_files.php",
   			data: {"dir":dir},
			success: function(data) {
				if(data.length != 0)
					generic_scenario_list = data.match(/[^\r\n]+/g);
			}
		});
	}

	function select_interface_changed(val)
	{
		update_scenario_list();
	}

	$("#config_select_interface").prop("selectedIndex", -1);

	$(function()
	{
		$('#add_interface_scenario').click(function() {
			var datarow = generaterow($("#config_select_interface").val());
			var rows = $('#jqxgrid').jqxGrid('getrows');
			var position = rows.length;
			for(var i=0, l=rows.length; i<l; i++)
			{
				if(rows[i]['interface'] == $("#config_select_interface").val())
				{
					$("#jqxgrid").jqxGrid('deleterow', i);
					position = i;
					break;
				}
			}
			var commit = $("#jqxgrid").jqxGrid('addrow', null, datarow, position);
		});
	});

	$(function()
	{
		$('#remove_interface_scenario').click(function()
      	{
			var selectedrowindex = $("#jqxgrid").jqxGrid('getselectedrowindex');
			var rowscount = $("#jqxgrid").jqxGrid('getdatainformation').rowscount;
			if (selectedrowindex >= 0 && selectedrowindex < rowscount) 
			{
				var id = $("#jqxgrid").jqxGrid('getrowid', selectedrowindex);
				var commit = $("#jqxgrid").jqxGrid('deleterow', id);
			}
		});
	});

    $(function()
    {
    	$('#save_rules_file').click(function() {
			if(save_rules_file_namebox.value.length == 0)
			{
				alert('Enter a filename before saving');
				return;
			}
    		$.ajax({
    			type: "POST",
				async: false,
    			url: "write.php",
    			data: {"F":'scenarios//'+save_rules_file_namebox.value,"D":rules_file_content.value},
    			success: function(data) {
					update_scenario_list();
				}
			});
      	});
    });
	
	function load_general_scenario_conf(data) 
	{
		data_array = data.split("\n");

		var rows = $('#jqxgrid').jqxGrid('getrows');
		for (var i=0, l=rows.length; i<l; i++)
			$("#jqxgrid").jqxGrid('deleterow', i);

		for (var i in data_array) 
		{
			if(data_array[i] == '')
				break;
			data_line = data_array[i].split(' ');

			var row = {};
			row["scenario"] = data_line[1];
			row["interface"] = [data_line[0]];
			var commit = $("#jqxgrid").jqxGrid('addrow', null, row, $('#jqxgrid').jqxGrid('getrows').length);
		}
	}
	
	function get_general_scenario_grid_data()
	{
		data = '';
		var rows = $('#jqxgrid').jqxGrid('getrows');
		for (var i=0, l=rows.length; i<l; i++)
			data += rows[i]["interface"]+' '+rows[i]["scenario"]+'\n';
		return data;
	}

	$(function()
	{
		$('#save_general_scenario_config_button').click(function() {
			if(save_general_scenario_config_namebox.value == '')
			{
				alert('Enter a file name');
				return;
			}
			file_data = get_general_scenario_grid_data();
			//alert(file_data);
			$.ajax({
    			type: "POST",
				async: false,
    			url: "write.php",
    			data: {"F":'general_scenarios//'+save_general_scenario_config_namebox.value,"D":file_data},
    			success: function(data) {
					update_scenario_list();
				}
			});
      	});
    });

	$(function()
	{
		$('#load_general_scenario_button').click(function() {
			$.ajax({ 
    			url: 'general_scenarios//'+load_general_scenario_select.value,
    			dataType: "text",
				cache: false,
    			success: function(data) {
      				load_general_scenario_conf(data);
				}
			});
		});
	});

	$(function()
	{
		$('#execute_shell_command_button').click(function() {
			$.ajax({ 
    			type: "POST",
				async: false,
    			url: "exec.php",
    			data: {"cmd": execute_shell_command_namebox.value},
    			success: function(data) {
      				// alert(data);
					execute_shell_output_area.value = jQuery.parseJSON(data);
				}
			});
		});
	});

</script>

<script type="text/javascript">
$(document).ready(function () {
	update_scenario_list();
	update_generic_scenario_list();

	// populate scenario select list
	var select = document.getElementById("load_rules_file_select");
	for(var i = 0; i < scenario_list.length; i++) {
    	select.options[select.options.length] = new Option(scenario_list[i], scenario_list[i]);
	}
	select = document.getElementById("load_general_scenario_select");
	for(var i = 0; i < generic_scenario_list.length; i++) {
    	select.options[select.options.length] = new Option(generic_scenario_list[i], generic_scenario_list[i]);
	}

	var theme = getDemoTheme();
	// prepare the data
	var data = {};
	var interfaces
	[
	];
	var scenarios
	[
	];
	
	var source =
	{
		localdata: data,
		datatype: "local",
		datafields:
		[
		{ name: 'interface', type: 'string' },
		{ name: 'scenario', type: 'string' }
		],

		addrow: function (rowid, rowdata, position, commit) {
			// synchronize with the server - send insert command
			// call commit with parameter true if the synchronization with the server is successful 
			//and with parameter false if the synchronization failed.
			// you can pass additional argument to the commit callback which represents the new ID if it is generated from a DB.
			commit(true);
		},
		deleterow: function (rowid, commit) 
		{
			// synchronize with the server - send delete command
			// call commit with parameter true if the synchronization with the server is successful 
			//and with parameter false if the synchronization failed.
			commit(true);
		},
		updaterow: function (rowid, newdata, commit) {
			// synchronize with the server - send update command
			// call commit with parameter true if the synchronization with the server is successful 
			// and with parameter false if the synchronization failed.
			commit(true);
		}
	};
	var dataAdapter = new $.jqx.dataAdapter(source);
	var listItems = [];
	var renderlist = function (row, column, value) 
	{
		var buildList = '<select id="select_itf_scenario_' + row + '" onchange="grid_select_scenario_changed(this.value, '+row+')">';
		for (var i = 0; i < scenario_list.length; i++) 
		{
			buildList += '<option value="'+ scenario_list[i] + '"';
			if(value == scenario_list[i])
				buildList += ' selected>';
			else
				buildList += '>';
			buildList += scenario_list[i] + '</option>';
		}
		buildList += '</select>';
		return buildList;
	}
	// initialize jqxGrid
	$("#jqxgrid").jqxGrid(
	{
		width: 500,
		height: 300,
		source: dataAdapter,
		theme: theme,
		columns:
		[
			{ text: 'Interface', datafield: 'interface', width: 250 },
			{ text: 'Scenario', datafield: 'scenario', width: 250, cellsrenderer: renderlist }
		]
	});
});

var grid_select_scenario_changed = function (scenario, index)
{
	var rows = $('#jqxgrid').jqxGrid('getrows');
	var row = {};
	row["scenario"] = scenario;
	row["interface"] = rows[index]['interface'];
	$("#jqxgrid").jqxGrid('updaterow', index, row);
}

var generaterow = function (itf)
{
	var row = {};

	row["scenario"] = scenario_list[0];
	row["interface"] = [itf];
	return row;
}

var getGeneralConfigValue = function ()
{
	var rows = $('#jqxgrid').jqxGrid('getrows');
	return rows;
}
</script>

<link rel="stylesheet" href="jqwidgets/styles/jqx.base.css" type="text/css" />
<script type="text/javascript" src="jqwidgets/jqxcore.js"></script>
<script type="text/javascript" src="jqwidgets/jqxdata.js"></script> 
<script type="text/javascript" src="jqwidgets/jqxbuttons.js"></script>
<script type="text/javascript" src="jqwidgets/jqxscrollbar.js"></script>
<script type="text/javascript" src="jqwidgets/jqxmenu.js"></script>
<script type="text/javascript" src="jqwidgets/jqxcheckbox.js"></script>
<script type="text/javascript" src="jqwidgets/jqxlistbox.js"></script>
<script type="text/javascript" src="jqwidgets/jqxdropdownlist.js"></script>
<script type="text/javascript" src="jqwidgets/jqxgrid.js"></script>
<script type="text/javascript" src="jqwidgets/jqxgrid.selection.js"></script> 
<script type="text/javascript" src="scripts/gettheme.js"></script>

</head>
<body>
<title>Aggregation test platform</title>
<div id="page_title">
	<h1>Aggregation test platform</h1>
</div>
<hr>
<div id="menu_choice">
	<h3>
	<input type="radio" id="static_menu_button" name="group1" value="static" onclick="change_menu(this.value)" checked> Static menu config
	<input type="radio" id="scenario_config_button" name="group1" value="config" onclick="change_menu(this.value)"> File menu config
	<input type="radio" id="scenario_editor_button" name="group1" value="editor" onclick="change_menu(this.value)"> Scenario editor
	</h3>	
	<hr>
</div>
<div id="static-conf">
<?php
	// retrieve interface list with this command
	error_reporting(E_ALL);
	foreach ($itf_list as $line) 
	{
		$bandwidth = 100000;
		$latency = 0;
		$loss = 0;
		$itf_ifb = str_replace("eth","ifb",$line);
		$cmd_netem = "sudo /sbin/tc qdisc ls dev $itf_ifb";
		$itf_netem_rules = array();
		exec($cmd_netem, $itf_netem_rules);
		if(count($itf_netem_rules) > 1)
		{
			sscanf(strstr($itf_netem_rules[0], "delay"),"delay %lfms loss %[^&]", $latency, $loss);
			$loss = chop($loss,'%');
			if(strrpos($itf_netem_rules[1], "Kbit"))
				sscanf(strstr($itf_netem_rules[1], "rate"),"rate %dKbit%[^&]", $bandwidth, $dummy);
			else
			{
				sscanf(strstr($itf_netem_rules[1], "rate"),"rate %dbit%[^&]", $bandwidth, $dummy);
				$bandwidth = $bandwidth / 1000;
			}
		}
		echo '<label for="bandwidth_form_'.$line.'">';
    	echo ' Bandwidth (in kbits): ';
    	echo '<input id="bandwidth_form_'.$line.'" onkeypress="return isNumberKey(event) type="text" value="'.$bandwidth.'" size=5 />';
		echo '</label>';
		echo '<label for="latency_form_'.$line.'">';
    	echo ' Delay (in ms): ';
    	echo '<input id="latency_form_'.$line.'" onkeypress="return isNumberKey(event) type="text" value="'.$latency.'" size=5 />';
		echo '</label>';
		echo '<label for="jitter_form_'.$line.'">';
    	echo ' Jitter (in ms): ';
    	echo '<input id="jitter_form_'.$line.'" onkeypress="return isNumberKey(event) type="text" value="0" size=5 />';
		echo '</label>';
		echo '<label for="loss_form_'.$line.'">';
    	echo ' Packets loss (in %): ';
    	echo '<input id="loss_form_'.$line.'" onkeypress="return isNumberKey(event) type="text" value="'.$loss.'" size=5 />';
		echo '</label>'."\n";
	
		echo ' <input type="button" value="Apply conf" onclick="apply_static_conf(bandwidth_form_'.$line.'.value, latency_form_'.$line.'.value, jitter_form_'.$line.'.value, loss_form_'.$line.'.value, \''.$line.'\')">'."\n";
		echo ' <input type="button" value="Reset" onclick="reset_interface(\''.$line.'\')">'."\n";
		echo $line;
		echo '<br><br>'."\n";
	} 
?>
</div>
<div id="scenario-editor">
	<label for="time_form">
    	Time (in seconds):
    	<input id="time_form" onkeypress="return isNumberKey(event)" value="0" type="text" size=10 />
	</label>
	<label for="bandwidth_form">
    	Bandwidth (in kbits):
    	<input id="bandwidth_form" onkeypress="return isNumberKey(event)" value="10000" type="text" size=10 />
	</label>
	<label for="latency_form">
    	Delay (in ms):
    	<input id="latency_form" onkeypress="return isNumberKey(event)" value="0" type="text" size=10 />
	</label>
	<label for="jitter_form">
    	Jitter (in ms):
    	<input id="jitter_form" onkeypress="return isNumberKey(event)" value="0" type="text" size=10 />
	</label>
	<label for="loss_form">
    	Packets loss (in %):
    	<input id="loss_form" onkeypress="return isNumberKey(event)" value="0" type="text" size=10 />
	</label>
	<input type="button" id="add_text_line" value="Add line">
	</br>
	<div id="itf-text-area-div">	
		<label for="itf_file">
			Rules file
			<form id="rules_file">
        		<textarea id="rules_file_content" rows="20" cols="70"></textarea>
			</form>
		</label>
	</div>
	</br></br></br></br>
	<div id="itf-save-load-div">
		</br></br>
		<label for="save_rules_file_namebox">
			File name
			<input id="save_rules_file_namebox" type="text" size=15 />
			<input type="button" id="save_rules_file" value="Save">
		</label>
		</br></br>
		<label for="load_rules_file">
			Load file
			<select id="load_rules_file_select" name="load_rules_file_select">
			<input type="button" id="load_rules_file_button" value="Load">
		</label>
		</br></br>
	</div>
</div>
<div id="scenario-config">
	<div id="scenario-menu-div">
		</br></br>
		<label>
			Interfaces list
			<select id="config_select_interface" name="config_select_interface" onchange="select_interface_changed(this.value)">
            	<?php
            		foreach ($itf_list as $line) {
                    	echo '<option value="'.$line.'">'.$line.'</option>'."\n";
                  	}
            	?>
            </select>
		</label>
		</br>
		<input type="button" id="add_interface_scenario" style="margin-top: 10px;" value="Add interface">
		</br>
		<input type="button" id="remove_interface_scenario" style="margin-top: 10px;" value="Remove interface">
	</div>
	<div id="general-scenario-resume">
        <div style="float: left;" id="jqxgrid">
        </div>
        <div style="margin-left: 20px; float: left;">
            <div>
                <label for="launch_general_scenario_config">
				Launch general scenario config
				<input id="launch_general_scenario_config" type="button" value="Launch" <?php if(!empty($script_process_list)) echo ' disabled="true"';?>/>
				</label>
				<input id="stop_general_scenario_config" type="button" value="Stop"<?php if(empty($script_process_list)) echo ' disabled="true"';?>/>
            </div>
			<div style="margin-top: 10px;">
                <label for="loop_general_scenario_checkbox">
				Loop <input id="loop_general_scenario_checkbox" type="checkbox" />
            </div>
            <div style="margin-top: 10px;">
                <label for="save_general_scenario_config_namebox">
				Save general scenario config name <input id="save_general_scenario_config_namebox" type="text" size=15 />
				<input id="save_general_scenario_config_button" type="button" value="Save" />
            </div>
            <div style="margin-top: 10px;">
				<label for="save_general_scenario_config_select">
				Load general scenario config file
                <select id="load_general_scenario_select" name="load_general_scenario_select"><input id="load_general_scenario_button" type="button" value="Load" />
            </div>
        </div>
	</div>
	<div style="clear: both; margin-left: 20px;">
		</br>
		<label for="execute_shell_command_namebox" style="float: left;">
			Execute shell command <input id="execute_shell_command_namebox" type="text" size=30 />
			<input id="execute_shell_command_button" type="button" value="Execute" />
		</label>
		<label for="execute_shell_output" style="float: left; margin-left: 20px;">
		Shell output
		<form id="execute_shell_output">
        		<textarea id="execute_shell_output_area" rows="20" cols="70"></textarea>
			</form>
		</label>
	</div>
</div>
</body>
</html>
