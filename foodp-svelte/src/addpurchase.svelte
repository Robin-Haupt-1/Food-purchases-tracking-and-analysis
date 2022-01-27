<script lang="ts">
    export let server;
    export let items;


    let metric
    let measurement
    let name
    let measure="g"

    function clear(){
    metric=undefined
    measurement=undefined
    name=undefined
    measure=undefined
    }
</script>



<input bind:value={name} class="form-control" name="itemname" id="itemname" placeholder="Name" required/>

<label class="col-sm-2 col-form-label" for="metrictype">Metric:</label>
<div id="metrictype" class="form-check-inline">
    <div class="form-check form-check-inline">
        <input
            class="form-check-input"
            type="radio"
            name="metric"
            id="metricweight"
            value={"weight"}
            bind:group={metric}

        />
        <label class="form-check-label" for="metricweight">Weight</label>
    </div>
    <div class="form-check form-check-inline">
        <input
            class="form-check-input"
            type="radio"
            name="metric"
            id="metricamount"
            value={"amount"}

            bind:group={metric}
        />
        <label class="form-check-label" for="metricamount">Amount</label>
    </div>
    <div class="form-check form-check-inline">
        <input
            class="form-check-input"
            type="radio"
            name="metric"
            id="metricother"
            value={"other"}

            bind:group={metric}
        />
        <label class="form-check-label" for="metricother">Other</label>
    </div>
</div><br>
{#if metric=="amount"}
<input type="number" bind:value={measurement} class="form-control" name="itemname" id="measurement" placeholder="Measurement" />

{/if}
<div id="metrictype" class="form-check-inline">
    <div class="form-check form-check-inline">
        <input
            class="form-check-input"
            type="radio"
            name="inlineRadioOptions"
            id="metricweight"
            value={"g"}
            bind:group={measure}
        />
        <label class="form-check-label" for="metricweight">g</label>
    </div>
    <div class="form-check form-check-inline">
        <input
            class="form-check-input"
            type="radio"
            name="inlineRadioOptions"
            id="metricamount"
            value={"ml"}
            bind:group={measure}
        />
        <label class="form-check-label" for="metricamount">ml</label>
    </div>
</div><p class="py-2">
<button class="btn btn-primary" on:click={()=>{
    // make sure all required fields are filled out
    if (!name||!metric){
        alert("Please fill out name and metric")
        return
    } 
    if(metric=="amount"&&(!measure||!measurement)){
        alert("Please fill out measure and measurement")
    }
    server.add_item(name,metric,measure,measurement)
    
}}>Save item</button>
<button class="btn btn-danger" on:click={clear}>Clear all fields</button></p>


