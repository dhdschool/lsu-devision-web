<script setup lang="ts">    
console.log("Hello World")
import { BCard } from 'bootstrap-vue-next';
</script>

<template>
  <main>
    <div>
      <h1 class="text-center">Contact Information</h1>
      <!--TODO: Organize in some sort of table.--> 
      <div>
        <b-card 
          border-variant="dark" 
          text-variant="dark" 
          bg-variant="light"
          title="Math Department Contacts"
          class="text-center"
        >
          <p>Peter Wolenski<br>
          <a href="mailto:wolenski@math.lsu.edu">wolenski@math.lsu.edu</a>
          </p>
        <p>Nadejda Drenska<br>
        <a href="mailto:ndrenska@lsu.edu">ndrenska@lsu.edu</a>
        </p>
        </b-card>
      </div>
    </div>
    <div>
      <b-card 
          border-variant="dark" 
          text-variant="dark" 
          bg-variant="light"
          title="GUI team contacts"
          class="text-center"
      >
        <div >  
          <p>Calvin Gavin<br>
          <a href="mailto:cgavin7@lsu.edu">cgavin7@lsu.edu</a>
          </p>
          <p>Alex Mensen-Johnson<br>
          <a href="mailto:Alex.Mensen-Johnson@lsu.edu">Alex.Mensen-Johnson@lsu.edu</a>
          </p>
          <p>Dow Draper<br>
          <a href="mailto:ddrape6@lsu.edu">ddrape6@lsu.edu</a>
          </p>
          <p>Gowri Sunka<br>
          <a href="gsunka1@lsu.edu">gsunka1@lsu.edu</a> 
          </p>
        </div>
      </b-card>
      </div>
  </main>
</template>

<style type="css"></style>