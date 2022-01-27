<script lang="ts">
	import 'bootstrap/dist/css/bootstrap.min.css';
  import Additem from '../additem.svelte'
  import Addpurchase from '../addpurchase.svelte'


	import { onMount } from 'svelte';
	import {serverip} from '../consts.js'

	import j from 'jquery';

    import b from 'bootstrap/dist/js/bootstrap.bundle.js';
    let stores=[]
    let items=[]
    let s
    class server{
        v:view
        constructor(v){
            this.v=v
        }

        all_stores(){
            fetch(serverip+"/stores/all").then(r=>r.json()).then(r=>{stores=r}).catch(e=>{alert(e)})
        } 
        all_items(){
            fetch(serverip+"/items/all").then(r=>r.json()).then(r=>{items=r}).catch(e=>{alert(e)})
        } 
        add_item(name,metric,measure,measurement){
          fetch(serverip+"/items/add?"+new URLSearchParams({"name":name,"metric":metric,"measure":measure,"measurement":measurement})).then(r=>r.text()).then(r=>{if (r!="success"){alert("Fehler")}}).catch(e=>{alert(e)})


        }
    }
    class view{

        constructor(){

        }

        refresh_stores(stores:Object){

        }
    }

	onMount(() => {

        let v=new view()
        s= new server(v)


		window.j = j;

		j(document).ready(function () {
			s.all_stores()
      setTimeout(s.all_items,100)
		});
	});

    
</script>

<svelte:head>
	<title>Enter purchase</title>
</svelte:head>
<main>
	<h1>Enter purchase</h1><br>
	<label class="col-sm-2 col-form-label" for="store">Geschäft:</label>
	<select class="form-select" name="store" id="store">
        {#each stores as store}
            <option value="{store["id"]}">{store["name"]}</option>
        {/each}
	</select>
  <br>
    <input type="text" class="form-control" id="datepicker" placeholder="Datum (YYYY-MM-DD)">

<br>
<p>

    <button class="btn btn-primary">Save purchase</button>
    <!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addItemModal">
    Add item
  </button>
  
  <!-- Modal -->
  <div class="modal fade "   data-bs-backdrop="static"  id="addItemModal" tabindex="-1" aria-labelledby="addItemModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Add Item</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <Additem server={s} />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
  <Addpurchase server={s} {items}/>

</main>

<style>
	div.spinner-border {
		height: 1em;
		width: 1em;
		display: none;
	}

	img#main-image {
		object-fit: scale-down;
		display: block;
		margin: auto;
		padding-bottom: 1em;
		opacity: 0;
		max-height: 100%;
		max-width: 100%;
	}

	main {
		max-width: 80%;
		margin: auto;
		padding: 1em;
		max-width: 1000px;
		margin: auto;
		margin-top: 40px;
	}
</style>
