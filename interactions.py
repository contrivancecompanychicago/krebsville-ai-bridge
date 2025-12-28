@bot.tree.command(name="move_to_zone_1", description="Exit Administration and enter the Triage Bay.")
async def move_to_zone_1(interaction: discord.Interaction):
    # 1. Check Firebase to see if the door is unlocked
    zone_data = db.collection('Zones').document('zone_0_administration').get().to_dict()
    
    if zone_data['systems']['door_controls']['bay_4_access'] == "GRANTED":
        # 2. Update Role to Medical Staff
        medical_role = discord.utils.get(interaction.guild.roles, name="Medical Staff")
        admin_role = discord.utils.get(interaction.guild.roles, name="System Admin")
        
        await interaction.user.add_roles(medical_role)
        await interaction.user.remove_roles(admin_role)
        
        await interaction.response.send_message("🚨 **DEPARTING ZONE 0.** Door seals disengaged. Good luck in Triage, Doctor.")
    else:
        await interaction.response.send_message("❌ **ACCESS DENIED.** Dr. Grant's terminal is still locked. Resolve the logic loop first.", ephemeral=True)
