*** Variables ***
${autosys_dev_url}    https://autosys.dev.com
${autosys_username_textbox}    //*[@type="text"]
${autosys_password_textbox}    //*[@type="password"]
${autosys_ecli_tab}    //*[contains(text(),'Enterprise Command Line')]
${autosys_ecli_server_textbox}    //*[@id="command_line_app_input_servers"]
${autosys_ecli_cmdline_textbox}    //*[@id="command_line_app_combobox_command_input"]
${autosys_ecli_execute_button}    //*[@id="command_line_app_button_command_execute"]
${autosys_ecli_cmdline_output_textarea}    //*[@id="command_line_app_command_output"]
${autosys_login_button}    //*[@type="button"]
${autosys_logout}    //*[@id="x-auto-82"]
${autosys_reset_button}    //*[@id="command_line_app_button_command_reset"]
${autosys_ecli_frame}    //*[@id="ECLI"]
${autosys_loader}    //*[@class="loading-indicator"]
${autosys_login_failure_message}    E15003: An error occurred during authentication. An invalid user name or password was entered
${autosys_login_failure_locked}    E15007: Login failed. The user account is locked
