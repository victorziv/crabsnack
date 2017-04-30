"use strict";
jQuery("#ibox_installation_steps_grid").jqGrid({
    
    url: "/api/v1.0/ibox/installation/steps",
    datatype: "json",
    jsonReader : { 
        root: "steps",
        page: "currpage",
        total: "totalpages",
        records: "totalrecords",
        repeatitems: false,
        id: "id"
    },

    {% include "ibox/installation/steps_colmodel.js" %}

    guiStyle: "bootstrap",
    iconSet: "fontAwesome",
    caption: "IBox Installation Steps",
    rownumbers: false,
    sortname: "priority",
    sortorder: "asc"
});




