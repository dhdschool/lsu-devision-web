<script setup lang="ts">

const MathContacts = [
  { id: 1, name: 'Peter Wolenski', email: 'wolenski@math.lsu.edu' },
  { id: 2, name: 'Nadejda Drenska', email: 'ndrenska@lsu.edu' },
]

const GuiContacts = [
  { id: 1, name: 'Calvin Gavin', email: 'cgavin7@lsu.edu' },
  { id: 2, name: 'Alex Mensen-Johnson', email: 'Alex.Mensen-Johnson@lsu.edu' },
  { id: 3, name: 'Dow Draper', email: 'ddrape6@lsu.edu' },
  {id: 4, name: 'Gowri Sunkara', email: 'gsunka1@lsu.edu' },
]

const Cards = [
  { id: 1, title: 'Math Department Contacts' , contacts: MathContacts },
  { id: 2, title: 'GUI Team Contacts', contacts: GuiContacts },
]
</script>

<template>
  <main>
    <h1 class="text-center">Contact Information</h1>
    <div v-for="card in Cards" :key="card.id" class="contact-card" >
      <h2 class="card-title">{{ card.title }}</h2>
      <div class="card-content" v-for="contact in card.contacts" :key="contact.id">
        <p>{{ contact.name }}<br>
          <a :href="'mailto:' + contact.email">{{ contact.email }}</a>
        </p>
      </div>
    </div>
  </main>
</template>

<style>

.container {
  display: justify-content;

}
</style>



